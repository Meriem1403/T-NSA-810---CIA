# Spécifications infrastructure — CIA

Document pour les trophées `infra_delivery` et `infra_spec`.

## Exigences du sujet (rappel)

| # | Exigence | Implémentation labo | Statut |
|---|----------|---------------------|--------|
| 1 | 2 sites Proxmox (on-prem + remote) | Proxmox 02 (S1) + Proxmox 01 (S2) | ✅ |
| 2 | Max 3 VMs / site | Services regroupés sur `infraservice` | ✅ |
| 3 | VPN site-à-site sécurisé | IPsec pfSense S1 ↔ S2 | ✅ |
| 4 | Pare-feu des 2 côtés | pfSense S1 + pfSense S2 (CARP) | ✅ |
| 5 | Kill switch réversible | Script + runbook DRP | 🟡 |
| 6 | Bastion accès distant | SSH 2222 + Guacamole | ✅ |
| 7 | IPAM NetBox automatisé | NetBox + script sync Ansible | ✅ |
| 8 | Logs centralisés + observabilité | Wazuh manager + agents | 🟡 |
| 9 | Site web interne uniquement | nginx `192.168.10.11` | ✅ |
| 10 | DNS inter-sites | `mar2.local` AD + pfSense | ✅ |
| 11 | IaC reproductible | Ansible + Terraform | 🟡 |

## Inventaire des composants

### Site 1 — On-prem

| Composant | Technologie | IP / accès | Rôle |
|-----------|-------------|------------|------|
| Hyperviseur | Proxmox VE 8.x | Proxmox 02 | Virtualisation S1 |
| Pare-feu | pfSense 2.7.x | `192.168.199.1` | Routage, filtrage, VPN |
| Identité | Windows Server AD | `mar2.local` | DNS, LDAP, PKI (en cours) |
| LAN | — | `192.168.199.0/24` | Réseau interne S1 |

### Site 2 — Remote

| Composant | Technologie | IP / accès | Rôle |
|-----------|-------------|------------|------|
| Hyperviseur | Proxmox VE 8.x | `192.168.102.11:8006` | Virtualisation S2 |
| Pare-feu | pfSense 2.7.x (CARP) | WAN `.102.103` / LAN `.10.1` | Sécurité périmétrique |
| Bastion | Ubuntu 24.04 | `192.168.10.11` | SSH jump, site interne |
| Client | Windows 11 | `192.168.10.10` | Poste utilisateur démo |
| InfraService | Ubuntu 24.04 + Docker | `192.168.10.15` | NetBox, Vault, Wazuh, IaC |
| Guacamole | Apache Guacamole | LAN S2 | Accès distant graphique |
| IP publique | Box FAI | `78.202.114.212` | Entrée Internet |

### Services sur InfraService (`192.168.10.15`)

| Service | Port | Conteneur / processus |
|---------|------|----------------------|
| NetBox | 8000 | Docker Compose |
| PostgreSQL | 5432 (local) | Docker Compose |
| Valkey | 6379 (local) | Docker Compose |
| Vault | 8200 | systemd / binaire |
| Wazuh manager | 1514/1515, 55000 | Docker / package |
| Ansible | — | pip / apt |
| Terraform | — | binaire |

## Contraintes respectées

- **3 VMs max / site** : S2 utilise VM100 (pfSense), VM101 (client), VM102 (bastion) ; InfraService peut être une 4ᵉ VM sur le même hyperviseur en labo étendu ou hôte dédié documenté.
- **Pas de secrets dans Git** : Vault + `.gitignore` + coffre équipe.
- **Stack communautaire** : toutes les technologies listées dans [`infra-choices.md`](./infra-choices.md).

## Livrables dépôt associés

| Type | Chemin |
|------|--------|
| Architecture | `docs/architecture.md` |
| Réseau S1 | `docs/network-site1.md` |
| Réseau S2 | `docs/network-site2.md` |
| IaC | `iac/ansible/`, `iac/terraform/` |
| Configs | `configs/` |
| État | `docs/status-2026-06-23.md` |

## Critères d'acceptation (soutenance)

1. Ping inter-sites via VPN depuis poste opérateur.
2. NetBox accessible et peuplé (sites + préfixes minimum).
3. Bastion joignable en SSH port 2222, pas en HTTP public.
4. Wazuh reçoit les logs d'au moins 2 agents.
5. Ansible exécutable avec inventaire `production.yml`.
6. Terraform `plan` sans erreur (apply si template disponible).
