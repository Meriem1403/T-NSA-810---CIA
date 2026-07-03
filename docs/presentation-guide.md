# Guide de présentation — soutenance CIA

Document pour le trophée `proj_presentation`.

## Format

| Élément | Durée suggérée |
|---------|----------------|
| Introduction & contexte | 2 min |
| Architecture (diagramme) | 3 min |
| Démo live infrastructure | 10 min |
| IaC & automatisation | 3 min |
| Sécurité, logs, incident | 4 min |
| Planning & conclusion | 2 min |
| **Total** | **~20 min** + questions |

## Génération automatique PowerPoint

```bash
./scripts/presentation/build.sh
```

Fichier produit : [`docs/presentations/CIA-Soutenance-T-NSA-810.pptx`](../presentations/CIA-Soutenance-T-NSA-810.pptx) (~23 slides).

Voir [`scripts/presentation/README.md`](../scripts/presentation/README.md).

## Structure des slides (recommandée)

| # | Slide | Trophées couverts |
|---|-------|-------------------|
| 1 | Titre — équipe, sujet T-NSA-810 CIA | `proj_presentation` |
| 2 | Contexte & objectifs du sujet | `infra_spec` |
| 3 | Choix techniques (tableau versions) | `infra_choices` |
| 4 | Diagramme architecture (PNG) | `diagram_delivery`, `diagram_quality` |
| 5 | Site 1 — réseau & AD | `network_spec1` |
| 6 | Site 2 — réseau & VMs | `network_spec2` |
| 7 | VPN IPsec — schéma tunnel | `network_vpn` |
| 8 | Pare-feu — règles clés | `network_firewall` |
| 9 | DNS `mar2.local` | `network_dns` |
| 10 | NetBox IPAM | `network_ip_mngmt` |
| 11 | Bastion & moindre privilège | `sec_bastion`, `sec_access` |
| 12 | Vault & gestion secrets | `sec_credentials` |
| 13 | Wazuh — centralisation & dashboards | `log_*` (×4) |
| 14 | Ansible + Terraform | `iac_delivery`, `iac_quality` |
| 15 | Kill switch & DRP | `incident_killswitch`, `incident_recovery` |
| 16 | Évolutivité (site N) | `infra_scalability` |
| 17 | Dépôt Git & organisation | `repo_*`, `proj_subdivision` |
| 18 | Planning & avancement 90 % | `proj_planning` |
| 19 | Conclusion & perspectives | — |

## Enchaînement démo live

Exécuter dans l'ordre (terminal préparé, VPN connecté) :

```bash
# 1. VPN (network_vpn)
ping -c 2 192.168.10.15

# 2. Site interne (sec_access)
curl -I http://192.168.10.11

# 3. Bastion (sec_bastion)
ssh -p 2222 bastion@78.202.114.212 "hostname"

# 4. Pare-feu (network_firewall)
nc -vz -G 3 78.202.114.212 22    # doit échouer
nc -vz -G 3 78.202.114.212 2222  # doit réussir

# 5. DNS (network_dns)
nslookup client1.site2.local 192.168.10.1

# 6. NetBox (network_ip_mngmt)
curl -I http://192.168.10.15:8000

# 7. Wazuh (log_centralisation)
ssh -p 2222 bastion@78.202.114.212 "logger 'CIA-SOUTENANCE-TEST'"

# 8. IaC (iac_delivery)
cd iac/terraform && terraform plan   # ou ansible --syntax-check

# 9. Kill switch (incident_killswitch) — si temps
# Désactiver IPsec pfSense, montrer ping KO, rollback
```

Puis montrer dans le navigateur :

- NetBox → sites et préfixes
- Wazuh → agents + événement test
- pfSense → IPsec status UP

## Captures à préparer (dossier `rapport/` hors repo)

| # | Capture | Trophée |
|---|---------|---------|
| 1 | Diagramme architecture | `diagram_*` |
| 2 | pfSense WAN rules + IPsec status | `network_firewall`, `network_vpn` |
| 3 | SSH bastion connecté | `sec_bastion` |
| 4 | curl timeout sans VPN | `sec_access` |
| 5 | NetBox préfixes | `network_ip_mngmt` |
| 6 | Wazuh agents + dashboard | `log_*` |
| 7 | Vault policies (sans secrets) | `sec_credentials` |
| 8 | terraform plan output | `iac_*` |
| 9 | Kill switch chronomètre | `incident_killswitch` |
| 10 | GitHub repo arborescence | `repo_content` |

## Conseils oraux

- **Montrer le dépôt GitHub** en introduction (`repo_doc`).
- **Ne jamais afficher** de mot de passe, token, PSK ou clé unseal.
- Expliquer le regroupement services sur `infraservice` (contrainte 3 VMs).
- Mentionner l'évolution OpenVPN → IPsec et ELK → Wazuh (maturité projet).
- Anticiper la question « que se passe-t-il si S2 tombe ? » → DRP [`drp-runbook.md`](./drp-runbook.md).

## Checklist veille de soutenance

- [ ] VPN connecté et testé
- [ ] NetBox et Wazuh accessibles
- [ ] Commandes démo copiées dans un fichier local
- [ ] Slides exportées PDF
- [ ] Captures insérées dans rapport / Excel
- [ ] `main` à jour sur GitHub
- [ ] Répétition chronométrée (< 20 min)

## Références

- [`demo-scenarios.md`](./demo-scenarios.md) — scénarios A→J
- [`trophees-validation.md`](./trophees-validation.md) — index 29 trophées
- [`criteres_evaluation_infrastructure.xlsx`](./criteres_evaluation_infrastructure.xlsx)
