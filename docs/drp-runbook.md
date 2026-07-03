# Runbook — Reprise après sinistre (DRP) et kill switch

Dernière mise à jour : **23 juin 2026**.

## Principes

- **Kill switch** : couper vite une exposition (VPN, bastion, VM isolée…) **avec** rollback documenté (< 10 min).
- **DRP** : ordre déterministe de reconstruction depuis ce dépôt + sauvegardes hors Git (Vault Raft, exports pfSense, dumps PostgreSQL).

---

## Kill switch réversible (Site 2 — procédure labo)

| Action | Lieu | Procédure |
|--------|------|-----------|
| Couper VPN IPsec | pfSense S2 `192.168.10.1` | `VPN > IPsec` — désactiver tunnel phase 1/2 **ou** règle WAN associée → Apply |
| Vérifier coupure | Client VPN | `ping 192.168.10.15` et `ping 192.168.102.11` doivent échouer |
| Couper SSH bastion public | Box + pfSense | Retirer NAT box `2222` **ou** désactiver port forward WAN→bastion |
| Isoler une VM | Proxmox / API Kill Switch | Arrêt VM ou coupure VLAN (en développement) |
| Bloquer une IP | pfSense / Wazuh | Règle firewall temporaire ou action automatisée (futur) |
| Rollback | Même écrans | Réactiver dans l’ordre inverse ; tester VPN puis `ssh -p 2222` |

**Objectif soutenance** : coupure + rollback en moins de **10 minutes** (chronomètre + captures).

Script d’aide : [`../scripts/kill-switch-s2.sh`](../scripts/kill-switch-s2.sh) (`status` / checklist `off` / `on`).
Guide : [`deploy-lab.md`](./deploy-lab.md) section 7.

### Kill switch via Wazuh (cible)

1. Alerte Wazuh déclenchée (brute-force SSH, scan, etc.).
2. Action automatisée vers API Kill Switch (`api.mar2.local`) — en développement.
3. Vérifier isolement + notification équipe.
4. Rollback documenté.

---

## Sauvegardes

| Composant | Fréquence | Emplacement | Restauration |
|-----------|-----------|-------------|--------------|
| Vault (Raft) | Automatique | Hors Git, stockage sécurisé | `vault operator raft snapshot restore` |
| NetBox / PostgreSQL | À industrialiser | Dump hors Git | `pg_restore` + restart NetBox |
| pfSense | Avant chaque changement majeur | Export XML sanitisé (coffre) | Import GUI |
| Proxmox VMs | vzdump (recommandé) | Stockage Proxmox / NFS | Restore VM |

---

## Ordre de reconstruction

1. Proxmox S1 / S2 (ISO ou restore vzdump)
2. Bridges / VLAN selon [`architecture.md`](./architecture.md)
3. VM pfSense + import config **sanitisée** (CARP si applicable)
4. VPN IPsec : PSK / certificats depuis Vault ou coffre
5. Tests `ping` / `traceroute` inter-sites
6. Active Directory `mar2.local` + DNS
7. Hôte **infraservice** (`192.168.10.15`) :
   - Docker (NetBox, PostgreSQL, Valkey)
   - Vault (init, unseal, restore snapshot Raft)
   - Wazuh manager + agents
   - Ansible, Terraform
8. Bastion S2 + clés SSH
9. Guacamole
10. NetBox : restore base + sync IPAM
11. Site interne nginx + test accès LAN/VPN uniquement
12. Nginx reverse proxy + certificats HTTPS (PKI AD)

---

## Validation post-rebuild

- [ ] Tunnel IPsec établi (site-à-site et client)
- [ ] DNS `mar2.local` fonctionnel
- [ ] NetBox accessible et à jour
- [ ] Vault unsealed, secrets accessibles via AppRole Ansible
- [ ] Agents Wazuh connectés, événements visibles
- [ ] Site interne non exposé Internet direct
- [ ] SSH externe via bastion (port 2222) uniquement
- [ ] Kill switch testé et réversible (< 10 min)
- [ ] Restauration NetBox/PostgreSQL testée

---

Les **secrets** (tokens, PSK IPsec, clés unseal Vault, AppRole Secret ID) ne figurent que dans le coffre d’équipe et HashiCorp Vault.
