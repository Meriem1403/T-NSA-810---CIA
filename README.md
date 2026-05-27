# T‑NSA‑810 — CIA : Infrastructure hybride sécurisée (Proxmox)

[![Status](https://img.shields.io/badge/status-in_progress-orange?style=for-the-badge)](./docs/gantt.md)
[![Infra](https://img.shields.io/badge/infra-Proxmox_|_pfSense_|_OpenVPN-blue?style=for-the-badge)](#pile-technique)
[![IaC](https://img.shields.io/badge/IaC-Ansible_|_Terraform-green?style=for-the-badge)](./iac)
[![Observabilité](https://img.shields.io/badge/observability-Elastic_|_Logs_|_Metrics-purple?style=for-the-badge)](./configs/elastic)
[![Git workflow](https://img.shields.io/badge/git-workflow_conventionné-000000?style=for-the-badge&logo=git)](./docs/git-workflow.md)

Dépôt officiel du projet **Cloud Infrastructure Architects (CIA)** : deux sites Proxmox (on‑prem + distant) reliés par VPN, protégés par des pare‑feu pfSense, pilotés par un IPAM NetBox, observés via Elasticsearch, avec bastion d’administration, DNS inter‑sites et procédures de reprise après sinistre.

> ℹ️ **Legacy :** l’ancien squelette **Flux / Kubernetes** est conservé sous `legacy/flux-bootstrap/` à titre d’archive ou de bonus GitOps. Il ne remplace pas les livrables Proxmox / VPN / pfSense demandés par le sujet.

---

## 🎯 Objectifs pédagogiques et fonctionnels

| Exigence | Où c’est traité dans le dépôt |
|----------|-------------------------------|
| 1 on‑prem + 1 remote Proxmox | `docs/architecture.md`, `iac/` |
| VPN site‑à‑site sécurisé (OpenVPN) | `configs/openvpn/`, schéma `docs/architecture.md` |
| Pare‑feu des deux côtés + kill switch | `configs/pfsense/`, `docs/drp-runbook.md` |
| Bastion (accès SSH distant contrôlé) | `docs/architecture.md`, `docs/demo-scenarios.md` |
| IPAM NetBox mis à jour automatiquement | `configs/netbox/`, `iac/ansible/` |
| Centralisation des journaux + observabilité (Elastic) | `configs/elastic/`, dashboards Kibana |
| Site web **interne uniquement** | `apps/` ou VM documentée dans `docs/architecture.md` |
| DNS forwarding inter‑sites | `docs/architecture.md`, zone / forwarders |
| IaC + documentation reproductible | `iac/`, `docs/` |

---

## 🧱 Pile technique

- **Virtualisation :** Proxmox VE (2 sites, max 3 VMs / site)
- **Réseau / Sécurité :** pfSense, OpenVPN (site‑to‑site), bastion SSH
- **IPAM :** NetBox (API + automatisation Ansible)
- **Observabilité :** Elasticsearch (stack ELK), Filebeat / Metricbeat (ou équivalent)
- **IaC :** Ansible (playbooks, rôles), Terraform (optionnel, provider Proxmox)

---

## 🗂 Arborescence du dépôt

```text
├── README.md                 # Vue d’ensemble + liens rapides
├── .gitignore
├── docs/
│   ├── architecture.md       # Schéma logique, VLAN, flux réseau, VPN, bastion, DNS
│   ├── drp-runbook.md       # Reprise après sinistre + kill switch réversible
│   ├── demo-scenarios.md    # Scénarios de démonstration (VPN, bastion, logs…)
│   ├── gantt.md             # Phases / jalons + backlog
│   ├── git-workflow.md      # Stratégie de branches et conventions de commits
│   └── checklist-evaluation.md
├── iac/
│   ├── ansible/              # Automatisation VMs / services / synchronisation NetBox
│   └── terraform/            # Optionnel : modules Proxmox & co
├── configs/
│   ├── openvpn/              # Extraits de config (sans clés ni secrets)
│   ├── pfsense/              # Exports / snippets de règles firewall & NAT
│   ├── netbox/               # Scripts API, modèles de préfixes
│   └── elastic/              # Pipelines, templates d’index, configs Filebeat
├── apps/                     # Application / site interne (ex. nginx + contenu statique)
└── legacy/
    └── flux-bootstrap/       # Ancien exemple Flux + Helm (podinfo)
```

---

## 🚀 Démarrage rapide

### 1. Cloner le dépôt

```bash
git clone https://github.com/Meriem1403/T-NSA-810---CIA.git
cd T-NSA-810---CIA
```

### 2. Comprendre l’architecture

1. Lire `docs/architecture.md` et adapter les **plages IP**, VLAN et noms de sites.
2. Valider le diagramme (Draw.io, Excalidraw, etc.) avec l’équipe / les encadrants.

### 3. Préparer l’automatisation Ansible

```bash
cd iac/ansible
ansible-playbook playbooks/site.yml --check   # ping de base sur tous les hôtes
```

Ensuite, ajouter vos rôles (OpenVPN, NetBox, agents Elastic…) et un inventaire local `inventory/production.yml` (non versionné) si besoin.

### 4. Ordre recommandé de déploiement

1. **Proxmox** : hyperviseurs + réseau (bridges, VLAN)  
2. **pfSense** : WAN / LAN / DMZ / Admin, règles minimales  
3. **VPN** : tunnel site‑à‑site fonctionnel (critère majeur)  
4. **Bastion** : accès SSH externalisé via jump host  
5. **NetBox** : IPAM et synchronisation automatique  
6. **Elastic** : centralisation des journaux + premiers dashboards  
7. **Site interne** : accessible uniquement depuis LAN/VPN  

---

## 📏 Contraintes sujet à respecter

- **Maximum 3 VMs par site Proxmox.**
- Pile technique **prises en charge par la communauté** (Proxmox VE, OpenVPN, pfSense, NetBox, Elastic…).
- Aucune donnée sensible (clés, `.ovpn`, mots de passe) dans Git : tout va dans un **coffre** (vault, gestionnaire de mots de passe, ansible‑vault).

Les correspondances détaillées critères ↔ livrables sont dans `docs/checklist-evaluation.md`.

---

## 🤝 Contribution (workflow Git)

> Détails dans `docs/git-workflow.md`.

- Branches de travail : `feature/<sujet>`, `fix/<sujet>`…
- Messages de commits explicites, en français ou anglais, au style impératif :
  - `feat(vpn): ajoute snippet server.conf sans secrets`
  - `docs(architecture): met à jour schéma VLAN admin`
- **Jamais** de secrets committés (clés, tokens, fichiers `.ovpn`, `*.tfstate`, etc.).

---

## 📚 Références

- Sujet / cahier des charges : `project.pdf` (fourni par la formation, à conserver hors dépôt public si nécessaire).
- Documentation officielles :
  - Proxmox VE — virtualisation
  - pfSense — pare‑feu / routage
  - OpenVPN — VPN site‑à‑site
  - NetBox — IPAM / DCIM
  - Elasticsearch / Elastic Stack — logs et métriques

---

## 🧪 Préparation de la soutenance

Avant chaque revue :

- Suivre la checklist `docs/demo-scenarios.md` (VPN, bastion, DNS, NetBox, logs…).
- Mettre à jour `docs/gantt.md` (avancement) et `docs/architecture.md` (diagramme exact du lab).
- Vérifier que la branche `main` reste **démontrable** à tout moment.

