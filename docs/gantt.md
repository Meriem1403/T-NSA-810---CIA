# Planification — phases CIA

Dernière mise à jour : **2026-05-29**

## Avancement par phase

| Phase | Jalons | Statut |
|-------|--------|--------|
| F0 Bootstrap | Repo, README, workflow Git | ✅ |
| F1 Revue scope | Diagramme PNG, backlog, grille Excel | ✅ |
| F2 Fondations S2 | pfSense, LAN, VMs 100–102 | ✅ |
| F3 VPN | Tunnel UP, ping/traceroute | ✅ |
| F4 Bastion + DNS + site interne S2 | SSH 2222, nginx, DNS | ✅ |
| F4 bis NetBox + Elastic S1 | Compose + playbooks `deploy-site1.yml` | 🟡 Exécuter sur VM `svc-s1` |
| F5 Observabilité | Filebeat bastion → Kibana | 🟡 `deploy-observability.yml` |
| F6 DRP / kill switch | Script + procédure pfSense | 🟡 Test chrono sur labo |
| F7 Finale | Rapport, captures, soutenance | ⏳ |

## Livrables dépôt (faits)

- `docs/architecture-diagram.png`
- `iac/docker/netbox/` + `iac/docker/elastic/`
- `iac/ansible/playbooks/deploy-site1.yml`, `deploy-observability.yml`
- `scripts/kill-switch-s2.sh`
- `docs/deploy-lab.md`

## Backlog restant (labo)

| # | Action |
|---|--------|
| 1 | Créer VM `svc-s1` (192.168.199.20) et lancer `deploy-site1.yml` |
| 2 | Token NetBox + `sync_from_inventory.py` |
| 3 | `deploy-observability.yml` + capture Kibana |
| 4 | Kill switch 10 min + captures pfSense |

## Journal des décisions

| Date | Décision |
|------|----------|
| 2026-05-29 | NetBox + Elastic regroupés sur une VM Docker S1 (quota 3 VMs/site) |
| 2026-05-29 | Diagramme PNG généré depuis Mermaid pour soutenance |
