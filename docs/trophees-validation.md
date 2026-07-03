# Guide de validation — 29 trophées CIA

Document central pour la plateforme Epitech **Course achievements**. Chaque trophée est mappé vers un livrable du dépôt, une preuve à fournir et une commande de démonstration.

**Dépôt :** [Meriem1403/T-NSA-810---CIA](https://github.com/Meriem1403/T-NSA-810---CIA)

| Légende | Signification |
|---------|---------------|
| ✅ | Documenté + démontrable sur le labo |
| 🟡 | Documenté, preuve live/capture à finaliser |
| 📸 | Capture d’écran requise pour le validateur |

---

## Infrastructure (4 trophées)

### `infra_delivery` — Livraison infrastructure

| Élément | Référence |
|---------|-----------|
| Doc | [`infra-specifications.md`](./infra-specifications.md) |
| État | [`status-2026-06-23.md`](./status-2026-06-23.md) |
| Déploiement | [`deploy-lab.md`](./deploy-lab.md) |

**Preuve :** deux sites Proxmox opérationnels, services InfraService déployés, démo live VPN + bastion + NetBox.

```bash
ping -c 2 192.168.10.15          # InfraService
curl -I http://192.168.10.15:8000 # NetBox
```

---

### `infra_spec` — Spécifications infrastructure

| Élément | Référence |
|---------|-----------|
| Doc | [`infra-specifications.md`](./infra-specifications.md) § Contraintes et exigences |
| Architecture | [`architecture.md`](./architecture.md) |
| Réseau S1/S2 | [`network-site1.md`](./network-site1.md), [`network-site2.md`](./network-site2.md) |

**Preuve :** tableau VMs, IP, rôles, contrainte 3 VMs/site, pile imposée par le sujet.

---

### `infra_scalability` — Évolutivité

| Élément | Référence |
|---------|-----------|
| Doc | [`architecture.md`](./architecture.md) § Évolutivité |
| Convention | LAN site N = `192.168.(10+N).0/24`, services `.15`, bastion `.11` |
| IPAM | NetBox — ajout site N documenté avant déploiement |

**Preuve :** expliquer à l’oral l’ajout d’un **site 3** sans refonte (nouveau préfixe, pfSense, tunnel IPsec, entrée NetBox).

---

### `infra_choices` — Choix techniques

| Élément | Référence |
|---------|-----------|
| Doc | [`infra-choices.md`](./infra-choices.md) |
| Justification | Stack communautaire, maintenance, intégration Vault/Ansible |

**Preuve :** tableau versions + justification Proxmox, pfSense, IPsec, NetBox, Wazuh, Vault.

---

## Diagrammes (2 trophées)

### `diagram_delivery` — Livraison schémas

| Élément | Référence |
|---------|-----------|
| PNG | [`architecture-diagram.png`](./architecture-diagram.png) |
| Source | [`architecture-diagram.mmd`](./architecture-diagram.mmd) |
| Guide | [`diagram-guide.md`](./diagram-guide.md) |

**Preuve :** fichier image dans `docs/` + schéma Mermaid versionné.

---

### `diagram_quality` — Qualité schémas

| Élément | Référence |
|---------|-----------|
| Doc | [`diagram-guide.md`](./diagram-guide.md) |
| Critères | Légendes IP, flux VPN, pare-feu, services nommés, deux sites visibles |

**Preuve :** diagramme lisible en soutenance ; flux Internet → pfSense → LAN → services explicites. 📸

---

## Infrastructure as Code (2 trophées)

### `iac_delivery` — Livraison IaC

| Élément | Référence |
|---------|-----------|
| Ansible | [`iac/ansible/`](../iac/ansible/) — playbooks, rôles, inventaire |
| Terraform | [`iac/terraform/`](../iac/terraform/) — provider Proxmox |
| Docker | [`iac/docker/`](../iac/docker/) — NetBox, Elastic (legacy) |
| Guide | [`iac-guide.md`](./iac-guide.md) |

**Preuve :**

```bash
cd iac/ansible && ansible-playbook playbooks/site.yml --syntax-check
cd iac/terraform && terraform init && terraform validate && terraform plan
```

---

### `iac_quality` — Qualité IaC

| Élément | Référence |
|---------|-----------|
| Doc | [`iac-guide.md`](./iac-guide.md) § Bonnes pratiques |
| Secrets | Variables `vault_*`, Vault AppRole, `.gitignore` |
| Idempotence | Rôles Ansible modulaires, handlers, tags |
| Terraform | Variables typées, `tfvars.example`, état hors Git |

**Preuve :** exécution `--check`, pas de secrets en clair, README par module.

---

## Réseau (6 trophées)

### `network_spec1` — Spécifications réseau site 1

| Élément | Référence |
|---------|-----------|
| Doc | [`network-site1.md`](./network-site1.md) |
| LAN | `192.168.199.0/24`, pfSense `.1`, AD `mar2.local` |

**Preuve :** plan d’adressage S1 + routage vers S2 via IPsec. 📸 pfSense S1

---

### `network_spec2` — Spécifications réseau site 2

| Élément | Référence |
|---------|-----------|
| Doc | [`network-site2.md`](./network-site2.md) |
| LAN | `192.168.10.0/24`, WAN `192.168.102.0/24` |

**Preuve :** VMs 100–102 + infraservice `.15`, NAT 2222, segmentation. 📸 pfSense S2

---

### `network_vpn` — VPN

| Élément | Référence |
|---------|-----------|
| Doc | [`demo-scenarios.md`](./demo-scenarios.md) § A |
| Config | Tunnels IPsec pfSense (PSK/cert hors Git) |
| Legacy | [`configs/openvpn/`](../configs/openvpn/) |

**Preuve :**

```bash
ping -c 3 192.168.10.15    # via tunnel
# pfSense > VPN > IPsec > Status : tunnel UP
```

📸 Statut IPsec + traceroute inter-sites

---

### `network_firewall` — Pare-feu

| Élément | Référence |
|---------|-----------|
| S1 | [`configs/pfsense/site1-lan-rules.md`](../configs/pfsense/site1-lan-rules.md) |
| S2 | [`configs/pfsense/site2-wan-rules.md`](../configs/pfsense/site2-wan-rules.md) |
| Démo | [`demo-scenarios.md`](./demo-scenarios.md) § D |

**Preuve :** deux pfSense, règles WAN/LAN documentées, tests `nc` (22 fermé, 2222 ouvert). 📸

---

### `network_dns` — DNS

| Élément | Référence |
|---------|-----------|
| Doc | [`configs/dns/forwarders.md`](../configs/dns/forwarders.md) |
| Domaine | `mar2.local` — AD + pfSense overrides |
| Démo | [`demo-scenarios.md`](./demo-scenarios.md) § E |

**Preuve :**

```bash
nslookup client1.site2.local 192.168.10.1
nslookup netbox.mar2.local
```

---

### `network_ip_mngmt` — Gestion des IP (IPAM)

| Élément | Référence |
|---------|-----------|
| NetBox | `http://192.168.10.15:8000` |
| Données | [`configs/netbox/sites-prefixes.example.yml`](../configs/netbox/sites-prefixes.example.yml) |
| Sync | [`configs/netbox/scripts/sync_from_inventory.py`](../configs/netbox/scripts/sync_from_inventory.py) |
| Playbook | `iac/ansible/playbooks/netbox-sync.yml` |

**Preuve :** UI NetBox avec sites/préfixes + exécution script sync. 📸

---

## Sécurité (3 trophées)

### `sec_access` — Contrôle d’accès / moindre privilège

| Élément | Référence |
|---------|-----------|
| Doc | [`secrets-and-access.md`](./secrets-and-access.md) |
| Matrice | Comptes dédiés, pas d’exposition LAN depuis Internet |
| Guacamole | Accès centralisé bastion |

**Preuve :** `curl` HTTP public timeout ; accès services uniquement LAN/VPN. [`demo-scenarios.md`](./demo-scenarios.md) § B

---

### `sec_bastion` — Bastion

| Élément | Référence |
|---------|-----------|
| VM | `bastion-s2` — `192.168.10.11` |
| Accès | SSH port `2222` (NAT), compte `bastion` |
| Démo | [`demo-scenarios.md`](./demo-scenarios.md) § C |
| IaC | Rôle Ansible `bastion` |

**Preuve :**

```bash
ssh -p 2222 bastion@78.202.114.212
```

📸 Connexion SSH + `sshd_config` (no root password)

---

### `sec_credentials` — Gestion des identifiants

| Élément | Référence |
|---------|-----------|
| Vault | `192.168.10.15:8200` — Raft, KV v2, AppRole |
| Doc | [`secrets-and-access.md`](./secrets-and-access.md) |
| `.gitignore` | Pas de `.ovpn`, `.env`, `*.tfstate`, tokens |

**Preuve :** démo lecture secret Ansible via AppRole (sans afficher le secret). Vault policies + snapshots Raft.

---

## Incident (2 trophées)

### `incident_killswitch` — Kill switch

| Élément | Référence |
|---------|-----------|
| Doc | [`drp-runbook.md`](./drp-runbook.md) |
| Script | [`scripts/kill-switch-s2.sh`](../scripts/kill-switch-s2.sh) |
| Démo | [`demo-scenarios.md`](./demo-scenarios.md) § H |

**Preuve :** couper tunnel IPsec, ping échoue, rollback < 10 min. 📸 + chronomètre

---

### `incident_recovery` — Reprise après sinistre (DRP)

| Élément | Référence |
|---------|-----------|
| Doc | [`drp-runbook.md`](./drp-runbook.md) § Ordre de reconstruction |
| Sauvegardes | Vault Raft snapshots, exports pfSense, dumps PostgreSQL |
| Validation | Checklist post-rebuild dans le runbook |

**Preuve :** expliquer l’ordre de reconstruction + test restauration (même partiel). 📸

---

## Logs & observabilité (4 trophées)

### `log_centralisation` — Centralisation des journaux

| Élément | Référence |
|---------|-----------|
| Stack | Wazuh manager sur `infraservice` |
| Agents | Bastion, hôtes supervisés |
| Guide | [`observability-guide.md`](./observability-guide.md) § Centralisation |

**Preuve :** agent connecté dans Wazuh UI, logs remontés < 2 min après événement test.

---

### `log_observability` — Observabilité

| Élément | Référence |
|---------|-----------|
| Doc | [`observability-guide.md`](./observability-guide.md) |
| Métriques | Wazuh agents, état cluster, alertes |
| Legacy | Filebeat → Elastic ([`configs/elastic/`](../configs/elastic/)) |

**Preuve :** dashboard Wazuh agents actifs + événements système visibles. 📸

---

### `log_analysis` — Analyse des journaux

| Élément | Référence |
|---------|-----------|
| Doc | [`observability-guide.md`](./observability-guide.md) § Analyse |
| Cas | Échecs SSH, scans, événements auth, alertes Wazuh |

**Preuve :** recherche filtre `CIA-WAZUH-TEST` ou alerte brute-force dans Wazuh. 📸

---

### `log_visuals` — Visualisations

| Élément | Référence |
|---------|-----------|
| Doc | [`observability-guide.md`](./observability-guide.md) § Dashboards |
| Dashboards | Connexions SSH/heure, top messages, répartition par agent |

**Preuve :** capture dashboard Wazuh en soutenance. 📸 (exporter si possible)

---

## Dépôt (3 trophées)

### `repo_practices` — Pratiques dépôt

| Élément | Référence |
|---------|-----------|
| Doc | [`git-workflow.md`](./git-workflow.md) |
| Branches | `main`, `feature/`, `fix/` |
| Commits | Style impératif, pas de secrets |
| `.gitignore` | Secrets, tfstate, inventory production |

**Preuve :** historique Git propre, PR avec tests manuels documentés.

---

### `repo_doc` — Documentation dépôt

| Élément | Référence |
|---------|-----------|
| Entrée | [`README.md`](../README.md) |
| Docs | Dossier [`docs/`](./) complet (15+ fichiers) |
| Index | Ce fichier |

**Preuve :** README à jour, liens vers tous les guides, badges statut.

---

### `repo_content` — Contenu dépôt

| Élément | Référence |
|---------|-----------|
| `configs/` | pfSense, DNS, NetBox, Wazuh, openvpn (legacy) |
| `iac/` | Ansible, Terraform, Docker |
| `apps/` | Site interne nginx |
| `scripts/` | Kill switch |
| `legacy/` | Flux bootstrap (archive) |

**Preuve :** arborescence complète versionnée, configs sanitisées sans secrets.

---

## Projet (3 trophées)

### `proj_subdivision` — Subdivision du travail

| Élément | Référence |
|---------|-----------|
| Doc | [`team-subdivision.md`](./team-subdivision.md) |
| Rôles | Répartition Meriem / Kévin / équipe |
| Backlog | [`gantt.md`](./gantt.md) § Backlog |

**Preuve :** tableau responsabilités par domaine (réseau, IaC, obs, doc).

---

### `proj_planning` — Planification

| Élément | Référence |
|---------|-----------|
| Gantt | [`gantt.md`](./gantt.md) |
| Phases | F0–F11 avec % avancement |
| État | [`status-2026-06-23.md`](./status-2026-06-23.md) |
| Excel | [`criteres_evaluation_infrastructure.xlsx`](./criteres_evaluation_infrastructure.xlsx) |

**Preuve :** jalons datés, backlog priorisé, 90 % avancement documenté.

---

### `proj_presentation` — Présentation

| Élément | Référence |
|---------|-----------|
| Guide | [`presentation-guide.md`](./presentation-guide.md) |
| Scénarios | [`demo-scenarios.md`](./demo-scenarios.md) |
| Durée | ~15–20 min + démo live chronométrée |

**Preuve :** support slides (hors repo) + enchaînement démo A→J + captures jointes.

---

## Checklist rapide avant validation plateforme

| # | Trophée | Fait ? |
|---|---------|--------|
| 1 | infra_delivery | ☐ |
| 2 | infra_spec | ☐ |
| 3 | infra_scalability | ☐ |
| 4 | infra_choices | ☐ |
| 5 | diagram_delivery | ☐ |
| 6 | diagram_quality | ☐ |
| 7 | iac_delivery | ☐ |
| 8 | iac_quality | ☐ |
| 9 | network_spec1 | ☐ |
| 10 | network_spec2 | ☐ |
| 11 | network_vpn | ☐ |
| 12 | network_firewall | ☐ |
| 13 | network_dns | ☐ |
| 14 | network_ip_mngmt | ☐ |
| 15 | sec_access | ☐ |
| 16 | sec_bastion | ☐ |
| 17 | sec_credentials | ☐ |
| 18 | incident_killswitch | ☐ |
| 19 | incident_recovery | ☐ |
| 20 | log_centralisation | ☐ |
| 21 | log_observability | ☐ |
| 22 | log_analysis | ☐ |
| 23 | log_visuals | ☐ |
| 24 | repo_practices | ☐ |
| 25 | repo_doc | ☐ |
| 26 | repo_content | ☐ |
| 27 | proj_subdivision | ☐ |
| 28 | proj_planning | ☐ |
| 29 | proj_presentation | ☐ |

---

## Ordre de démonstration recommandé (soutenance)

1. Architecture (diagramme) → `diagram_*`
2. Réseau S1 + S2 → `network_spec*`
3. VPN live → `network_vpn`
4. Pare-feu tests → `network_firewall`
5. Bastion SSH → `sec_bastion`, `sec_access`
6. DNS + NetBox → `network_dns`, `network_ip_mngmt`
7. Vault (secrets) → `sec_credentials`
8. Wazuh (logs) → `log_*`
9. Ansible + Terraform → `iac_*`
10. Kill switch → `incident_killswitch`
11. DRP → `incident_recovery`
12. Dépôt + planning → `repo_*`, `proj_*`
