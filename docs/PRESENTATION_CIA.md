# CIA — T-NSA-810

**Équipe :** Meriem ZAHZOUH · Kévin SEMERCIYAN — Epitech Master 2 NSA  
**Dépôt :** [github.com/Meriem1403/T-NSA-810---CIA](https://github.com/Meriem1403/T-NSA-810---CIA)  
**Document technique :** [`T-NSA-810-CIA_Document_technique_infrastructure (2).docx`](./T-NSA-810-CIA_Document_technique_infrastructure%20(2).docx)

---

## Synthèse

**CIA** (*Cloud Infrastructure Architects*) — infrastructure cybersécurité hybride : deux sites **Proxmox**, **pfSense** × 2, **IPsec** site-à-site, **Active Directory `mar2.local`**, **Wazuh**, bastion **Guacamole**, **Vault**, **NetBox**, **Ansible / Terraform**.

| Champ | Valeur |
|-------|--------|
| Domaine | `mar2.local` |
| Architecture | Deux sites Proxmox interconnectés par VPN IPsec |
| Sécurité | pfSense, HTTPS, Wazuh, Vault, Guacamole, segmentation VLAN |
| Exploitation | NetBox, Ansible, Terraform, sauvegardes et PRA |

**Ce qui n'est pas encore en place :** segmentation VLAN complète du document technique (labo simplifié), Nginx HTTPS finalisé, OpenVPN + LDAPS en production, Kill Switch API, `terraform apply`, dashboards Wazuh finaux, sauvegardes NetBox/PostgreSQL automatisées, LDAP applicatif Vault/NetBox.

---

## Document technique ↔ labo actuel

| Élément | Cible (doc. technique) | Labo actuel | Écart |
|---------|------------------------|-------------|-------|
| Site 1 — Production | Proxmox-01 `192.168.156.11`, VLAN 10 `10.10.10.0/24` | Proxmox 02, LAN `192.168.199.0/24` | VLAN 10/30/40 non déployés ; pas de serveur Apps/DB `10.10.10.52` |
| Site 2 — Sécurité | Proxmox-02 `192.168.102.11`, VLAN 20 `10.20.20.0/24` | Proxmox 01, LAN `192.168.10.0/24` | Un seul LAN à la place de 4 VLAN |
| Wazuh | VM dédiée `10.20.20.13` | Sur InfraService `192.168.10.15` | Pas de VM Wazuh séparée (contrainte 3 VMs/site) |
| Guacamole | `10.20.20.14` | Bastion SSH `.11` + Guacamole LAN/VPN | IP et VM dédiée non alignées sur le doc. |
| Infra-services | `10.20.20.15` | `192.168.10.15` | Adressage différent ; services regroupés |
| Nginx HTTPS | Reverse proxy sur Infra-services | Non finalisé | Accès HTTP direct ; certificats PKI AD à faire |
| Kill Switch | API `:9000` | Script + coupure VPN manuelle pfSense | API non opérationnelle ; pas d'intégration Wazuh/pfSense auto |
| VPN utilisateurs | OpenVPN S1 + LDAPS AD | IPsec client | OpenVPN documenté mais pas la solution labo |
| pfSense S2 WAN | `192.168.102.103` | `192.168.102.103` | Aligné |
| IPsec site-à-site | VLAN 10/20/30/40 | Tunnel S1 ↔ S2 | Fonctionnel ; pas tous les réseaux du doc. |
| IP publique | — | `78.202.114.212` | — |

---

## Accès

| Service | Cible | Labo | Écart |
|---------|-------|------|-------|
| NetBox | HTTPS `10.20.20.15` | `http://192.168.10.15:8000` | Pas de HTTPS ; nom `netbox.mar2.local` partiel |
| Vault | `:8200` ou HTTPS | `http://192.168.10.15:8200` | HTTP seul ; LDAP non branché |
| Wazuh | `10.20.20.13` | InfraService / `wazuh.mar2.local` | Dashboards et alertes à finaliser |
| Guacamole | `10.20.20.14` | LAN / VPN | SSO et durcissement incomplets |
| Kill Switch | `:9000` | — | Non déployé |
| pfSense S2 | `10.20.20.1` | `https://192.168.10.1` | Adresse LAN différente |
| Bastion SSH | — | `ssh -p 2222 bastion@78.202.114.212` | OK en labo |
| Site interne | Nginx HTTPS | `http://192.168.10.11` | HTTP seul ; pas via reverse proxy |
| AD / DNS | `10.10.10.100` | `mar2.local` | LDAPS et PKI non finalisés |

---

# §1 — Objectif et périmètre

Infrastructure opérationnelle couvrant virtualisation, routage, filtrage, identité, DNS, supervision, secrets, accès admin, automatisation et procédures d'exploitation.

| Domaine | Composants |
|---------|------------|
| Virtualisation | Deux Proxmox, VMs pfSense, AD, services |
| Réseau | pfSense × 2, NAT, VLAN, IPsec, OpenVPN (documenté) |
| Identité | AD `mar2.local`, DNS interne |
| Supervision | Wazuh (manager, indexer, dashboard, agents) |
| Accès | Guacamole, SSH bastion, Nginx HTTPS |
| Secrets | Vault KV v2, AppRole, snapshots Raft |
| Documentation | NetBox |
| Automatisation | Ansible + Terraform |
| Incident | Kill Switch, PRA, sauvegardes |

**Écarts :** serveur Apps/DB non déployé ; VLAN Backup (30) et Utilisateurs (40) absents du labo ; Kill Switch et PRA partiellement testés ; sauvegardes NetBox/AD non industrialisées.

---

# §2 — Architecture générale

| Site | Rôle | Services |
|------|------|----------|
| **Site 1** | Production, identité | pfSense, AD/DNS, Apps/DB, DHCP, OpenVPN |
| **Site 2** | Sécurité, administration | pfSense, Wazuh, Guacamole, Vault, NetBox, Nginx, Ansible, Terraform, Kill Switch |

Interconnexion **IPsec** entre les deux sites. Proxmox sur WAN public ; pfSense virtualisés avec WAN sur bridge public et LAN/trunk pour les VLAN.

Schéma : [architecture-diagram.png](./architecture-diagram.png)

**Écarts :** le diagramme PNG reflète le labo (`192.168.10.x`) plus que les VLAN `10.x.x.x` du document technique ; serveur Apps/DB et OpenVPN S1 absents du labo ; Nginx et Kill Switch non visibles sur le schéma actuel.

---

# §3 — Plan d'adressage et VLAN

## VLAN (document technique)

| VLAN | Nom | Site 1 | Site 2 | Usage |
|------|-----|--------|--------|-------|
| 10 | Production | `10.10.10.0/24` | — | AD/DNS, Apps/DB |
| 20 | Security | — | `10.20.20.0/24` | Wazuh, Guacamole, Infra-services |
| 30 | Backup | `10.30.10.0/24` | `10.30.20.0/24` | Sauvegardes |
| 40 | Utilisateurs | `10.40.10.0/24` | `10.40.20.0/24` | Clients, OpenVPN |

## Site 1

| Service | IP cible |
|---------|----------|
| Proxmox-01 | `192.168.156.11` |
| pfSense-01 (prod) | `10.10.10.1` |
| AD / DNS | `10.10.10.100` |
| Apps / DB | `10.10.10.52` |

## Site 2

| Service | IP cible |
|---------|----------|
| Proxmox-02 | `192.168.102.11` |
| pfSense-02 (security) | `10.20.20.1` |
| Wazuh | `10.20.20.13` |
| Guacamole | `10.20.20.14` |
| Infra-services | `10.20.20.15` |

## Services sur Infra-services

Nginx (HTTPS) · Vault (`:8200`) · NetBox · Terraform · Ansible · Kill Switch (`:9000`)

**Écarts :** labo = LAN unique `192.168.10.0/24` et `192.168.199.0/24` sans trunk VLAN ; Apps/DB `10.10.10.52` inexistant ; Wazuh et Guacamole non sur IP dédiées ; sync NetBox pas toujours à jour avec le labo réel.

---

# §4 — Réseau, routage et VPN

## Matrice de flux (cible)

| Flux | Source → Destination | Usage |
|------|---------------------|-------|
| IPsec | VLAN S1 ↔ VLAN S2 | Inter-sites chiffré |
| OpenVPN | Internet → S1 VLAN 40 | Utilisateurs + LDAPS |
| Wazuh | Production → `10.20.20.13` | Agents |
| Bastion | Réseaux autorisés → Guacamole | SSH/RDP centralisé |
| Sauvegardes | VLAN 30 ↔ VLAN 30 distant | Backup inter-sites |

```bash
ping -c 3 192.168.10.15
traceroute 192.168.10.15
```

**Écarts :** OpenVPN + LDAPS non opérationnels (IPsec client utilisé à la place) ; flux VLAN 30 Backup non implémentés ; routage inter-VLAN du document technique non reproduit ; agents Wazuh pas déployés sur toutes les VMs prévues (notamment production S1).

---

# §5 — Règles de pare-feu

Politique moindre privilège : deny par défaut, deny final journalisé.

Règles documentées : WAN (IPsec, OpenVPN, anti-bogon), IPsec inter-sites, VLAN 10/20/30/40, blocage VLAN 40 → VLAN 20 sauf Guacamole.

```bash
nc -vz -G 5 78.202.114.212 2222    # OK
nc -vz -G 5 78.202.114.212 22      # fermé
nc -vz -G 5 78.202.114.212 80      # fermé
```

**Écarts :** règles VLAN 10/20/30/40 du document technique non toutes appliquées en labo (un LAN plat S2) ; règles IPsec inter-VLAN partielles ; deny final journalisé à vérifier sur pfSense S1 ; export pfSense S1 pas systématique.

---

# §6 — Services d'identité

| Élément | Détail |
|---------|--------|
| Domaine | `mar2.local` |
| DNS | AD/DNS (cible `10.10.10.100`) |
| Flux | LDAP, LDAPS, Kerberos, DNS, SMB, RDP |
| VPN utilisateurs | OpenVPN S1 → LDAPS AD |

```bash
nslookup mar2.local
nslookup netbox.mar2.local 192.168.10.1
```

**Écarts :** LDAPS et PKI AD non finalisés ; OpenVPN utilisateur non en prod ; enregistrements DNS `vault.mar2.local` / `wazuh.mar2.local` pas tous résolus hors VPN ; intégration LDAP Vault et NetBox (~40 %) non terminée.

---

# §7 — Sécurité périmétrique et accès

## Contrôle d'accès

Pas d'exposition LAN directe depuis Internet. Services web via Nginx HTTPS (cible). Site interne accessible VPN/LAN uniquement.

```bash
curl -I http://192.168.10.11              # VPN → 200
curl -I --connect-timeout 5 http://192.168.10.11  # sans VPN → timeout
```

## Bastion Guacamole

Accès SSH/RDP centralisé. Labo : SSH port 2222 + Guacamole en LAN/VPN.

```bash
ssh -p 2222 bastion@78.202.114.212
```

## Vault

KV v2, policies, AppRole Ansible, snapshots Raft. Secrets hors Git.

**Écarts :** Nginx reverse proxy HTTPS non finalisé (~50 %) ; site interne en HTTP direct ; Guacamole sans SSO/LDAPS ; Vault en HTTP ; pas de certificats PKI AD sur les services web.

---

# §8 — Supervision (Wazuh)

| Composant | Rôle |
|-----------|------|
| Manager | Analyse, corrélation |
| Indexer | Stockage |
| Dashboard | Visualisation |
| Agents | Collecte sur serveurs |

```bash
ssh -p 2222 bastion@78.202.114.212 "logger 'CIA-SOUTENANCE-TEST'"
```

**Écarts :** dashboards personnalisés non finalisés ; alertes SSH/scans à configurer ; agents manquants sur certaines VMs ; pas de lien Kill Switch ↔ Wazuh ; `log_visuals` dépend de dashboards encore incomplets.

---

# §9 — Vault

| Fonctionnalité | État |
|----------------|------|
| KV v2 | ✅ |
| Policies | ✅ |
| AppRole Ansible | ✅ |
| Snapshots Raft | ✅ |
| LDAP auth | ❌ non finalisé |

**Écarts :** authentification LDAP applicative non branchée ; accès encore en HTTP ; rotation automatique des secrets non démontrée en live.

---

# §10 — NetBox

Référentiel : sites, préfixes, IP, VLAN, services.

`http://192.168.10.15:8000`

**Écarts :** préfixes VLAN `10.x.x.x` du document technique pas tous renseignés ; sync automatique inventaire ↔ labo à relancer ; pas de HTTPS ; sauvegarde PostgreSQL non automatisée.

---

# §11 — Automatisation (Ansible / Terraform)

| Outil | État |
|-------|------|
| Ansible | ✅ playbooks, rôles, lecture Vault validée |
| Terraform | 🟡 `validate`/`plan` OK, `apply` bloqué |

```bash
ansible-playbook playbooks/site.yml --syntax-check
terraform init && terraform validate && terraform plan
```

**Écarts :** pas de template Cloud-Init Ubuntu sur Proxmox → `terraform apply` impossible ; chaîne Terraform → Ansible post-déploiement non démontrée bout en bout ; certains rôles Ansible pas rejoués sur tout le parc.

---

# §12 — Sauvegardes et PRA

| Composant | Méthode | État |
|-----------|---------|------|
| Vault | Snapshots Raft | ✅ |
| NetBox / PostgreSQL | — | ❌ non automatisé |
| Wazuh | — | 🟡 partiel |
| pfSense | Export XML | 🟡 manuel |
| AD | Sauvegarde système | 🟡 incomplet |

Ordre reconstruction : Proxmox → réseau → pfSense → VPN → AD → InfraService → Guacamole → tests.

**Écarts :** scénarios PRA (perte AD, Vault, VPN, site) documentés mais pas tous testés ; restauration NetBox jamais validée en conditions réelles ; exports pfSense S1 irréguliers.

---

# §13 — Kill Switch

Cible : API `10.20.20.15:9000` — blocage IP, isolation segment, coupure VPN, traçabilité.

Procédure labo actuelle : désactivation manuelle IPsec pfSense + script `kill-switch-s2.sh`.

**Écarts :** API Kill Switch ~30 % (structure initiale seulement) ; pas d'actions automatiques pfSense/Proxmox/Wazuh ; test chronométré < 10 min non validé ; pas de retour arrière automatisé.

---

# §14 — Diagrammes

Livrables : [architecture-diagram.png](./architecture-diagram.png), [architecture-diagram.mmd](./architecture-diagram.mmd), schémas dans le document technique.

**Écarts :** PNG aligné sur le labo simplifié, pas sur les VLAN `10.x.x.x` ; pas de schéma séparé VLAN Backup/Utilisateurs ; matrice de flux complète uniquement dans le `.docx`.

---

# §15 — Dépôt Git

Dépôt : document technique, guides Markdown, configs sanitisées, IaC, scripts. Workflow branches `feature/`, commits conventionnels.

| Membre | Domaines |
|--------|----------|
| Meriem ZAHZOUH | Proxmox S2, pfSense, bastion, site interne, document technique |
| Kévin SEMERCIYAN | InfraService, Vault, Wazuh, Ansible, Terraform, NetBox |

**Écarts :** certaines configs pfSense en labo pas re-exportées dans `configs/` ; diagramme Mermaid pas régénéré après dernières modifs labo ; document technique `.docx` pas versionné dans Git (fichier local `docs/`).

---

# Synthèse des 29 trophées

| Trophée | État | Limite / écart |
|---------|------|----------------|
| `infra_delivery` | ✅ | Labo simplifié vs architecture cible VLAN |
| `infra_spec` | ✅ doc / 🟡 labo | VLAN 10/20/30/40 non tous déployés |
| `infra_scalability` | ✅ doc | Site 3 non implémenté (modèle documenté seulement) |
| `infra_choices` | ✅ | — |
| `diagram_delivery` | ✅ | — |
| `diagram_quality` | 🟡 | Schéma = labo, pas VLAN cible complets |
| `iac_delivery` | 🟡 | Terraform livré mais `apply` bloqué |
| `iac_quality` | ✅ | — |
| `network_spec1` | ✅ doc / 🟡 labo | Apps/DB et VLAN S1 incomplets |
| `network_spec2` | ✅ doc / 🟡 labo | VLAN Security non segmenté en labo |
| `network_vpn` | ✅ IPsec / 🟡 OpenVPN | OpenVPN + LDAPS non en prod |
| `network_firewall` | 🟡 | Règles VLAN doc. pas toutes en labo |
| `network_dns` | 🟡 | LDAPS, résolution inter-sites partielle |
| `network_ip_mngmt` | 🟡 | Sync NetBox pas toujours à jour |
| `sec_access` | ✅ | Nginx HTTPS manquant |
| `sec_bastion` | 🟡 | Guacamole OK mais SSO incomplet |
| `sec_credentials` | ✅ | LDAP Vault/NetBox non finalisé |
| `incident_killswitch` | 🟡 | API absente ; coupure VPN manuelle seulement |
| `incident_recovery` | 🟡 | PRA documenté, tests restauration incomplets |
| `log_centralisation` | 🟡 | Agents pas sur tout le parc |
| `log_observability` | 🟡 | Fonctionnel, alertes à finaliser |
| `log_analysis` | 🟡 | Filtres à configurer |
| `log_visuals` | 🟡 | Dashboards non finalisés |
| `repo_practices` | ✅ | — |
| `repo_doc` | ✅ | `.docx` hors Git |
| `repo_content` | ✅ | — |
| `proj_subdivision` | ✅ | — |
| `proj_planning` | ✅ | ~90 % global |
| `proj_presentation` | — | Ce document |

---

## Commandes utiles (labo, VPN requis)

```bash
ping -c 2 192.168.10.15
curl -I http://192.168.10.11
nc -vz -G 5 78.202.114.212 2222
ssh -p 2222 bastion@78.202.114.212 "hostname"
nslookup netbox.mar2.local 192.168.10.1
curl -I http://192.168.10.15:8000
ssh -p 2222 bastion@78.202.114.212 "logger 'CIA-SOUTENANCE-TEST'"
cd iac/terraform && terraform plan
```

---

## Références

| Fichier | Contenu |
|---------|---------|
| [T-NSA-810-CIA_Document_technique_infrastructure (2).docx](./T-NSA-810-CIA_Document_technique_infrastructure%20(2).docx) | Architecture cible |
| [status-2026-06-23.md](./status-2026-06-23.md) | État détaillé |
| [trophees-validation.md](./trophees-validation.md) | Index trophées |
| [drp-runbook.md](./drp-runbook.md) | PRA et kill switch |
| [architecture.md](./architecture.md) | Architecture labo |
