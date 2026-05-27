# T-NSA-810 — CIA : Infrastructure hybride sécurisée (Proxmox)

Dépôt officiel du projet **Cloud Infrastructure Architects (CIA)** : deux sites Proxmox (on-prem + distant), interconnexion VPN, pare-feu (pfSense), IPAM (NetBox), observabilité (Elasticsearch / stack ELK), bastion, DNS et procédures de reprise.

> **Note :** L’ancien squelette **Flux / Kubernetes** est conservé sous `legacy/flux-bootstrap/` à titre d’archive ou de bonus GitOps. Il ne remplace pas les livrables Proxmox/VPN/pfSense demandés par le sujet.

## Objectifs (rappel du cahier des charges)

| Exigence | Où c’est traité dans le dépôt |
|----------|-------------------------------|
| Site 1 + Site 2 Proxmox | `docs/architecture.md`, `iac/` |
| VPN site-à-site sécurisé (OpenVPN) | `configs/openvpn/`, diagramme |
| Pare-feu des deux côtés + kill switch | `configs/pfsense/`, `docs/drp-runbook.md` |
| Bastion (accès distant contrôlé) | `docs/architecture.md`, démo |
| IPAM NetBox mis à jour automatiquement | `configs/netbox/`, playbooks Ansible |
| Centralisation journaux + observabilité (Elasticsearch) | `configs/elastic/` |
| Site web uniquement en interne | `apps/` ou VM dédiée documentée |
| DNS forwarding inter-sites | `docs/architecture.md` |
| IaC + documentation reproductible | `iac/`, `docs/` |

## Arborescence

```text
├── README.md                 # Ce fichier
├── .gitignore
├── docs/
│   ├── architecture.md       # Schéma logique + liste des flux réseau
│   ├── drp-runbook.md       # Reprise après sinistre + kill switch réversible
│   ├── demo-scenarios.md    # Scénarios de démonstration soutenance
│   ├── gantt.md             # Phases / jalons (tableau + suivi)
│   ├── git-workflow.md      # Stratégie de branches et commits
│   └── checklist-evaluation.md
├── iac/
│   ├── ansible/              # Automatisation VMs / services / sync NetBox
│   └── terraform/            # Optionnel : Proxmox provider, etc.
├── configs/
│   ├── openvpn/              # Extraits de config (sans clés)
│   ├── pfsense/              # Exports / snippets de règles
│   ├── netbox/               # Scripts API, modèles de préfixes
│   └── elastic/              # Pipelines, templates d’index, Filebeat
├── apps/                     # Application / site interne (ex. nginx + contenu statique)
└── legacy/
    └── flux-bootstrap/       # Ancien exemple Flux + Helm (podinfo)
```

## Démarrage rapide pour l’équipe

1. Lire `docs/architecture.md` puis compléter les adresses réelles des sites et VLANs.
2. Suivre `docs/git-workflow.md` pour les branches et éviter tout secret dans Git.
3. Déployer / configurer d’abord le **tunnel VPN** puis les pare-feu, puis DNS, puis services.
4. Centraliser secrets dans un **coffre** (vault, gestionnaire, ansible-vault) — jamais en clair.
5. Exécuter les scénarios de `docs/demo-scenarios.md` avant la revue finale.

## Contraintes sujet à respecter

- **Maximum 3 VMs par site** Proxmox.
- Pile technique **maintenue par la communauté** : Proxmox VE, OpenVPN, pfSense, NetBox, Elasticsearch, etc.

## Contribution

Voir `docs/git-workflow.md`. Messages de commits explicites, PR par fonctionnalité, pas de fichier de secrets suivis par Git.

## Références

- Cahier des charges projet : fichier `project.pdf` (fourri par la formation ou copié hors dépôt public si besoin).
