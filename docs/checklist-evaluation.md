# Grille évaluation ↔ livrables ↔ 29 trophées

Index complet : [`trophees-validation.md`](./trophees-validation.md)

| Trophée | Critère | Livrable dépôt / démo |
|---------|---------|----------------------|
| `infra_delivery` | Cloud hybride fonctionnel | README, `infra-specifications.md`, démo live |
| `infra_spec` | Spécifications | `infra-specifications.md`, `architecture.md` |
| `infra_scalability` | Évolutivité | `architecture.md` § Évolutivité |
| `infra_choices` | Choix stack | `infra-choices.md` |
| `diagram_delivery` | Schémas livrés | `architecture-diagram.png`, `.mmd` |
| `diagram_quality` | Qualité schémas | `diagram-guide.md` |
| `iac_delivery` | Livraison IaC | `iac/ansible/`, `iac/terraform/` |
| `iac_quality` | Qualité IaC | `iac-guide.md` |
| `network_spec1` | Réseau site 1 | `network-site1.md`, `configs/pfsense/site1-*` |
| `network_spec2` | Réseau site 2 | `network-site2.md`, `configs/pfsense/site2-*` |
| `network_vpn` | VPN | `demo-scenarios.md` § A, IPsec pfSense |
| `network_firewall` | Pare-feux x2 | `configs/pfsense/`, `demo-scenarios.md` § D |
| `network_dns` | DNS | `configs/dns/forwarders.md`, `demo-scenarios.md` § E |
| `network_ip_mngmt` | IPAM | `configs/netbox/`, NetBox UI, sync script |
| `sec_access` | Moindre privilège | `secrets-and-access.md`, `demo-scenarios.md` § B |
| `sec_bastion` | Bastion | `architecture.md`, `demo-scenarios.md` § C |
| `sec_credentials` | Secrets | Vault, `secrets-and-access.md` |
| `incident_killswitch` | Kill switch | `drp-runbook.md`, `scripts/kill-switch-s2.sh` |
| `incident_recovery` | DRP | `drp-runbook.md` § reconstruction |
| `log_centralisation` | Centralisation logs | Wazuh, `observability-guide.md` |
| `log_observability` | Observabilité | Wazuh agents, `configs/wazuh/` |
| `log_analysis` | Analyse logs | `observability-guide.md` § Analyse |
| `log_visuals` | Visualisations | Dashboards Wazuh, captures |
| `repo_practices` | Pratiques dépôt | `git-workflow.md`, `.gitignore` |
| `repo_doc` | Doc dépôt | `README.md`, dossier `docs/` |
| `repo_content` | Contenu dépôt | `configs/`, `iac/`, `apps/`, `scripts/` |
| `proj_subdivision` | Subdivision travail | `team-subdivision.md` |
| `proj_planning` | Planification | `gantt.md`, `status-2026-06-23.md`, Excel |
| `proj_presentation` | Présentation | `presentation-guide.md`, `demo-scenarios.md` |

État détaillé : [`status-2026-06-23.md`](./status-2026-06-23.md) — **90 %**.
