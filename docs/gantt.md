# Planification — phases CIA

Dernière mise à jour : **2026-05-29**

## Avancement par phase

| Phase | Jalons | Statut |
|-------|--------|--------|
| F0 Bootstrap | Repo, README, workflow Git | ✅ |
| F1 Revue scope | Diagramme, backlog, grille Excel | 🟡 |
| F2 Fondations S2 | pfSense, LAN 10.0/24, VMs 100–102 | ✅ |
| F3 VPN | Tunnel UP, ping/traceroute | ✅ |
| F4 Bastion + DNS + site interne | SSH 2222, nginx, DNS overrides | ✅ |
| F4 bis NetBox | VM S1 + sync API | ⏳ |
| F5 Elastic | Cluster S1 + Filebeat bastion | ⏳ |
| F6 DRP / kill switch | Test coupure VPN < 10 min | ⏳ |
| F7 Finale | S1 complet, rapport, soutenance | ⏳ |

## Backlog prioritaire

| # | Titre | Responsable |
|---|-------|-------------|
| 1 | Déployer NetBox sur site S1 + lancer `netbox-sync.yml` | Équipe |
| 2 | VM Elastic + `filebeat.yml` sur bastion S2 | Équipe |
| 3 | Compléter diagramme site S1 dans `architecture.md` | Équipe |
| 4 | Test kill switch + capture pfSense | Pote / S2 |
| 5 | Export PNG depuis `architecture-diagram.mmd` | Équipe |

## Journal des décisions

| Date | Décision |
|------|----------|
| 2026-05-28 | Site S2 : 3 VMs max (pfSense, Client, bastion) |
| 2026-05-29 | SSH public via box **2222** → pfSense → bastion (pas 22 direct) |
| 2026-05-29 | Site interne nginx sur bastion `192.168.10.11` |
