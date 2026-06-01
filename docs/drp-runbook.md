# Runbook — Reprise après sinistre (DRP) et kill switch

## Principes

- **Kill switch** : couper vite une exposition (VPN WAN, DMZ…) **avec** rollback documenté.
- **DRP** : ordre déterministe de reconstruction depuis ce dépôt + sauvegardes hors Git.

---

## Kill switch réversible (Site 2 — procédure labo)

| Action | Lieu | Procédure |
|--------|------|-----------|
| Couper inbound OpenVPN WAN | pfSense S2 `192.168.10.1` | `Firewall > Rules > WAN` — désactiver règle **UDP 1194** → Apply |
| Vérifier coupure | Client VPN | `ping 192.168.102.11` doit échouer |
| Couper SSH bastion public | Box + pfSense | Retirer NAT box `2222` **ou** désactiver port forward WAN→bastion |
| Rollback | Même écrans | Réactiver règles dans l’ordre inverse ; tester VPN puis `ssh -p 2222` |

**Objectif soutenance** : coupure + rollback en moins de **10 minutes** (chronomètre + captures).

## Kill switch réversible (générique)

| Action | Lieu | Procédure (adapter) |
|--------|------|---------------------|
| Couper inbound OpenVPN WAN | pfSense S2 WAN | Désactiver règle autorisant le port OU arrêter le service VPN |
| Isoler VLAN Admin | pfSense | Suspension temporaire règles LAN→Admin |

**Rollback** : réactiver règle / service comme export sauvegardé ; test connexion.

---

## Ordre de reconstruction

1. Proxmox S1 / S2 (ISO ou restore vzdump)
2. Bridges / VLAN selon `architecture.md`
3. VM pfSense + import config **sanitisée**
4. OpenVPN : CA + certificats depuis coffre
5. Tests `ping` / `traceroute` inter-sites
6. Bastion + clés
7. NetBox + restore base si besoin
8. Elasticsearch + agents
9. Site interne + test accès LAN/VPN uniquement

---

## Validation post-rebuild

- [ ] VPN établi
- [ ] DNS entre sites
- [ ] NetBox à jour
- [ ] Logs centralisés visibles
- [ ] Site interne non exposé Internet direct
- [ ] SSH externe via bastion uniquement

---

Les **secrets** ne figurent que dans le coffre d’équipe (noms d’entrées référencés ici si besoin).
