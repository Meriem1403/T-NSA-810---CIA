# Grille évaluation ↔ livrables

| Critère | Livrable dépôt / démo |
|---------|----------------------|
| Cloud hybride fonctionnel | Démo vivante README point d’entrée ops |
| Services requis majeurs | doc table objectifs README |
| Évolutivité | conventions adresses site N dans `architecture.md` |
| Choix stack maintenus | Versions listées hors secrets |
| Schémas | `architecture.md` + fichier image exporté conseillé `docs/` |
| IaC quantité majoritaire | dossiers `iac/` remplis et exécutés |
| Spécifs réseau 1 et 2 | `demo-scenarios.md` sections B+C |
| VPN | section A demos + configs OpenVPN sanitized |
| Pare-feux x2 | `configs/pfsense/` exports snippets |
| DNS | exemple forwarders fichier md ou conf template |
| IPAM NetBox automatisé | playbooks + `configs/netbox/` |
| Moindre privilège / bastion / secrets | architecture + drp + coffre externe |
| Kill switch + DRP | `drp-runbook.md` |
| Logs centralisés + obs complète + analyse + visuels | `configs/elastic/` + captures Kibana |
| Pratiques dépôt | ce fichier + workflow + branches |
| Doc dépôt | README + docs/ |
| Contenu dépôt | configs + iac + apps |
| Gantt / backlog | `gantt.md` + liens issues |
| Présentation orale | slides hors repo + appui `demo-scenarios.md` |
