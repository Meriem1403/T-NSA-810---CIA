# T‑NSA‑810 — CIA : Infrastructure hybride sécurisée (Proxmox)

[![Status](https://img.shields.io/badge/status-90%25-green?style=for-the-badge)](./docs/trophees-validation.md)
[![Infra](https://img.shields.io/badge/infra-Proxmox_|_pfSense_|_IPsec-blue?style=for-the-badge)](#pile-technique)
[![IaC](https://img.shields.io/badge/IaC-Ansible_|_Terraform_|_Vault-green?style=for-the-badge)](./iac)
[![Observabilité](https://img.shields.io/badge/observability-Wazuh_|_agents-purple?style=for-the-badge)](./docs/architecture.md#observabilité)
[![Git workflow](https://img.shields.io/badge/git-workflow_conventionné-000000?style=for-the-badge&logo=git)](./docs/git-workflow.md)

Dépôt officiel du projet **Cloud Infrastructure Architects (CIA)** : deux sites Proxmox (on‑prem + distant) reliés par VPN IPsec, protégés par des pare‑feu pfSense (CARP), pilotés par un IPAM NetBox, observés via Wazuh, avec bastion d’administration, Active Directory `mar2.local`, Guacamole, gestion des secrets HashiCorp Vault, DNS inter‑sites et procédures de reprise après sinistre.

> **Trophées Epitech (29/29) :** guide complet dans [`docs/trophees-validation.md`](./docs/trophees-validation.md).

> **État d'avancement :** voir [`docs/status-2026-06-23.md`](./docs/status-2026-06-23.md) et [`docs/gantt.md`](./docs/gantt.md) (mise à jour 23 juin 2026, ~90 %).

> ℹ️ **Legacy :** l’ancien squelette **Flux / Kubernetes** est sous `legacy/flux-bootstrap/`. Les playbooks **Elastic/Filebeat** et les notes **OpenVPN** (`configs/openvpn/`, `configs/elastic/`) correspondent à une phase initiale du labo ; la supervision courante repose sur **Wazuh**.

---

## Objectifs pédagogiques et fonctionnels

| Exigence | Où c’est traité dans le dépôt |
|----------|-------------------------------|
| 1 on‑prem + 1 remote Proxmox | `docs/architecture.md`, `iac/terraform/` |
| VPN site‑à‑site sécurisé (IPsec) | `docs/architecture.md`, `docs/demo-scenarios.md` § A |
| VPN client‑à‑site | `docs/demo-scenarios.md` § A |
| Pare‑feu des deux côtés + kill switch | `configs/pfsense/`, `docs/drp-runbook.md`, `scripts/kill-switch-s2.sh` |
| Bastion / accès distant contrôlé | `docs/architecture.md`, Guacamole, SSH port 2222 |
| IPAM NetBox mis à jour automatiquement | `configs/netbox/`, `iac/ansible/` |
| Centralisation des journaux + observabilité (Wazuh) | `docs/architecture.md`, agents Wazuh |
| Site web **interne uniquement** | `apps/internal-site/`, nginx sur bastion S2 |
| DNS forwarding inter‑sites | `docs/architecture.md`, domaine `mar2.local` |
| Gestion des secrets (Vault) | `docs/secrets-and-access.md`, AppRole Ansible |
| IaC + documentation reproductible | `iac/`, `docs/` |

---

## Pile technique

| Couche | Technologie | État |
|--------|-------------|------|
| Virtualisation | Proxmox VE (2 nœuds) | ✅ |
| Réseau / Sécurité | pfSense + CARP, IPsec, bastion SSH | ✅ |
| Identité | Active Directory `mar2.local`, Guacamole | 🟡 LDAPS/PKI à finaliser |
| IPAM | NetBox (Docker, API + Ansible) | ✅ |
| Secrets | HashiCorp Vault (Raft, KV v2, AppRole) | ✅ |
| Observabilité | Wazuh + agents | 🟡 Dashboards/alertes à finaliser |
| Données | PostgreSQL, Valkey | ✅ |
| IaC | Ansible, Terraform (provider Proxmox) | 🟡 `terraform apply` en attente de template |
| Reverse proxy | Nginx + HTTPS (PKI AD) | 🟡 À finaliser |

**Hôte services centralisés :** `infraservice` — `192.168.10.15` (NetBox, Vault, Ansible, Terraform, PostgreSQL, Valkey).

---

## Arborescence du dépôt

```text
├── README.md
├── docs/
│   ├── architecture.md           # Schéma, VLAN, VPN, services
│   ├── architecture-diagram.png  # Diagramme soutenance
│   ├── status-2026-06-23.md      # État d’avancement (Kévin)
│   ├── gantt.md                  # Planification et backlog
│   ├── demo-scenarios.md         # Scénarios de démonstration
│   ├── deploy-lab.md             # Guide déploiement labo
│   ├── drp-runbook.md            # DRP + kill switch
│   ├── secrets-and-access.md     # Matrice d'accès et coffre
│   ├── checklist-evaluation.md   # Grille ↔ 29 trophées
│   └── trophees-validation.md    # Index complet trophées Epitech
├── iac/
│   ├── ansible/                  # Playbooks et rôles
│   ├── docker/                   # Compose NetBox / Elastic (legacy)
│   └── terraform/                # Provider Proxmox + module VM
├── configs/
│   ├── dns/                      # Forwarders mar2.local
│   ├── pfsense/                  # Règles S1 + S2
│   ├── netbox/                   # Scripts API IPAM
│   ├── wazuh/                    # Supervision SIEM
│   ├── elastic/                  # Legacy ELK / Filebeat
│   └── openvpn/                  # Legacy phase initiale OpenVPN
├── apps/internal-site/           # Site web interne (nginx)
├── scripts/
│   ├── kill-switch-s2.sh
│   └── presentation/           # Génération PowerPoint auto
├── docs/presentations/         # CIA-Soutenance-T-NSA-810.pptx
└── legacy/flux-bootstrap/        # Archive GitOps Kubernetes
```

---

## Démarrage rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/Meriem1403/T-NSA-810---CIA.git
cd T-NSA-810---CIA
```

### 2. Comprendre l’architecture

1. Lire [`docs/architecture.md`](./docs/architecture.md) et [`docs/status-2026-06-23.md`](./docs/status-2026-06-23.md).
2. Vérifier le diagramme [`docs/architecture-diagram.png`](./docs/architecture-diagram.png).

### 3. Services principaux (domaine `mar2.local`)

| Service | URL labo | Port |
|---------|----------|------|
| NetBox | `http://192.168.10.15:8000` | 8000 |
| Vault | `http://192.168.10.15:8200` | 8200 |
| Wazuh | `https://wazuh.mar2.local` (ou IP) | 443 |
| Guacamole | via pfSense / LAN | — |
| Site interne | `http://192.168.10.11` | 80 |

### 4. Automatisation Ansible

```bash
cd iac/ansible
cp inventory/example.inventory.yml inventory/production.yml
# Secrets : vault.yml local ou HashiCorp Vault AppRole (voir secrets-and-access.md)
ansible-playbook -i inventory/production.yml playbooks/site.yml --check
```

### 5. Terraform (Proxmox)

```bash
cd iac/terraform
terraform init && terraform validate && terraform plan
# Prérequis : template Cloud-Init `ubuntu-template` sur Proxmox
```

Guide complet : [`docs/deploy-lab.md`](./docs/deploy-lab.md).

---

## Contraintes sujet

- **Maximum 3 VMs par site Proxmox** (services regroupés sur `infraservice` si besoin).
- Pile **maintenue par la communauté** (Proxmox, pfSense, IPsec, NetBox, Wazuh, Vault…).
- **Aucun secret dans Git** : coffre d’équipe + HashiCorp Vault + `ansible-vault`.

Correspondances critères ↔ livrables : [`docs/checklist-evaluation.md`](./docs/checklist-evaluation.md).

---

## Contribution (workflow Git)

> Détails dans [`docs/git-workflow.md`](./docs/git-workflow.md).

- Branches : `feature/<sujet>`, `fix/<sujet>`…
- Commits au style impératif : `docs(architecture): …`, `feat(terraform): …`
- Jamais de secrets, `*.tfstate`, `.ovpn`, tokens ou clés d’unseal dans Git.

---

## Préparation de la soutenance

1. Valider les **29 trophées** : [`docs/trophees-validation.md`](./docs/trophees-validation.md).
2. Suivre [`docs/demo-scenarios.md`](./docs/demo-scenarios.md) et [`docs/presentation-guide.md`](./docs/presentation-guide.md).
3. Mettre à jour [`docs/gantt.md`](./docs/gantt.md) après chaque jalon.
4. Joindre captures (pfSense, Wazuh, NetBox) au rapport / Excel.
5. Vérifier que `main` reste démontrable.
