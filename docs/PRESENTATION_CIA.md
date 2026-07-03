# CIA — T-NSA-810

**Équipe :** Meriem ZAHZOUH · Kévin SEMERCIYAN · Fabio TILLET — Epitech Master 2 NSA  
**Dépôt :** [github.com/Meriem1403/T-NSA-810---CIA](https://github.com/Meriem1403/T-NSA-810---CIA)  
**Document technique :** [`T-NSA-810-CIA_Document_technique_infrastructure (2).docx`](./T-NSA-810-CIA_Document_technique_infrastructure%20(2).docx)

---

## Synthèse

Infrastructure cybersécurité d'entreprise : deux sites **Proxmox** virtualisés, **pfSense** sur chaque site, tunnel **IPsec** site-à-site, domaine **Active Directory `mar2.local`**, supervision **Wazuh**, bastion **Guacamole**, gestion des secrets **Vault**, documentation **NetBox**, automatisation **Ansible / Terraform**, **Kill Switch** et **PRA**.

| Champ | Valeur |
|-------|--------|
| Domaine | `mar2.local` |
| Architecture | Deux sites Proxmox interconnectés par VPN IPsec |
| Sécurité | pfSense, HTTPS, Wazuh, Vault, Guacamole, segmentation VLAN |
| Exploitation | NetBox, Ansible, Terraform, sauvegardes et PRA |
| Avancement | **100 %** — hors authentification **LDAP Vault** (en cours) |

**Point restant :** intégration LDAP sur Vault (auth utilisateurs via Active Directory). Tout le reste est déployé et opérationnel.

---

## Accès et URLs

| Service | Adresse | Accès |
|---------|---------|-------|
| NetBox | `https://netbox.mar2.local` | Reverse proxy Nginx sur Infra-services |
| Vault | `https://vault.mar2.local` ou `10.20.20.15:8200` | KV v2, AppRole Ansible |
| Wazuh | `https://wazuh.mar2.local` | Dashboard, agents, alertes |
| Guacamole | `https://10.20.20.14` | Bastion SSH/RDP centralisé |
| Kill Switch API | `https://api.mar2.local` ou `10.20.20.15:9000` | Réaction sécurité |
| Nginx (reverse proxy) | `10.20.20.15` / HTTPS | Publication centralisée |
| pfSense Site 1 | WAN `192.168.156.13` | Pare-feu production |
| pfSense Site 2 | WAN `192.168.102.103` · GW VLAN 20 `10.20.20.1` | Pare-feu sécurité |
| Proxmox Site 1 | `https://192.168.156.11:8006` | Hyperviseur S1 |
| Proxmox Site 2 | `https://192.168.102.11:8006` | Hyperviseur S2 |
| AD / DNS | `10.10.10.100` | Domaine `mar2.local` |
| Apps / DB | `10.10.10.52` | Applications + MariaDB |
| OpenVPN | Pool `10.40.10.x` | Accès utilisateurs + LDAPS AD |

---

# §1 — Objectif et périmètre

Infrastructure **opérationnelle, sécurisée, supervisée et documentée**, proche d'un cas d'usage entreprise. Chaque composant est intégré dans une architecture cohérente — système complet, pas une juxtaposition d'outils.

| Domaine | Composants déployés |
|---------|---------------------|
| Virtualisation | Deux hôtes Proxmox, VMs pfSense, AD, Apps/DB, services |
| Réseau | pfSense × 2, NAT, VLAN 10/20/30/40, IPsec, OpenVPN SSL/TLS |
| Identité | AD `mar2.local`, DNS interne, LDAPS (VPN et AD) |
| Supervision | Wazuh manager, indexer, dashboard, agents |
| Accès | Guacamole bastion, Nginx HTTPS |
| Secrets | Vault KV v2, policies, AppRole, snapshots Raft |
| Documentation | NetBox (sites, VLAN, IP, services, flux) |
| Automatisation | Ansible + Terraform (provisionnement Proxmox) |
| Incident | Kill Switch API, PRA, sauvegardes |

---

# §2 — Architecture générale

| Site | Rôle | Services principaux |
|------|------|---------------------|
| **Site 1** | Production, identité, services métier | pfSense, AD/DNS, Apps/DB MariaDB, clients DHCP, OpenVPN |
| **Site 2** | Sécurité, administration, infrastructure | pfSense, Wazuh, Guacamole, Vault, NetBox, Nginx, Ansible, Terraform, Kill Switch |

Interconnexion **IPsec** entre les deux sites. Les hôtes **Proxmox** restent sur le réseau public/WAN (`192.168.156.11` et `192.168.102.11`). Les **pfSense** sont virtualisés : WAN sur le bridge public du Proxmox, LAN/trunk pour distribuer les VLAN aux VMs.

Schéma : [architecture-diagram.png](./architecture-diagram.png)

---

# §3 — Plan d'adressage et VLAN

Le plan distingue adresses **publiques/WAN** (Proxmox + WAN pfSense) et **VLAN internes** portés par les pfSense virtualisés. Segmentation limitée aux usages présents : production, sécurité, sauvegarde, utilisateurs.

## Synthèse des VLAN

| VLAN | Nom | Site 1 | Site 2 | Passerelle | Usage |
|------|-----|--------|--------|------------|-------|
| 10 | Production | `10.10.10.0/24` | — | `10.10.10.1` | AD/DNS, Apps/DB, services métier |
| 20 | Security | — | `10.20.20.0/24` | `10.20.20.1` | Wazuh, Guacamole, Infra-services |
| 30 | Backup | `10.30.10.0/24` | `10.30.20.0/24` | `.1` par site | Sauvegardes et restauration |
| 40 | Utilisateurs | `10.40.10.0/24` | `10.40.20.0/24` | `.1` par site | Postes clients, pool OpenVPN |

## Site 1 — Production et identité

| Machine / Service | Rôle | VLAN | IP | Passerelle |
|-------------------|------|------|-----|------------|
| Proxmox-01 | Hyperviseur (héberge pfSense-01) | WAN | `192.168.156.11` | Réseau public |
| pfSense-01 WAN | Accès externe | WAN | `192.168.156.13` | — |
| pfSense-01 | Gateway Production | 10 | `10.10.10.1` | — |
| pfSense-01 | Gateway Backup | 30 | `10.30.10.1` | — |
| pfSense-01 | Gateway Utilisateurs | 40 | `10.40.10.1` | — |
| AD / DNS | Domaine `mar2.local` | 10 | `10.10.10.100` | `10.10.10.1` |
| Serveur Apps / DB | Applications + MariaDB | 10 | `10.10.10.52` | `10.10.10.1` |
| Postes clients | DHCP | 40 | `10.40.10.x` | `10.40.10.1` |
| OpenVPN SSL/TLS | Accès distant + LDAPS | 40 | Pool `10.40.10.x` | `10.40.10.1` |

## Site 2 — Sécurité et administration

| Machine / Service | Rôle | VLAN | IP | Passerelle |
|-------------------|------|------|-----|------------|
| Proxmox-02 | Hyperviseur (héberge pfSense-02) | WAN | `192.168.102.11` | Réseau public |
| pfSense-02 WAN | Accès externe | WAN | `192.168.102.103` | — |
| pfSense-02 | Gateway Security | 20 | `10.20.20.1` | — |
| pfSense-02 | Gateway Backup | 30 | `10.30.20.1` | — |
| pfSense-02 | Gateway Utilisateurs | 40 | `10.40.20.1` | — |
| Wazuh | Supervision sécurité | 20 | `10.20.20.13` | `10.20.20.1` |
| Guacamole | Bastion SSH/RDP | 20 | `10.20.20.14` | `10.20.20.1` |
| Infra-services | Vault, NetBox, Nginx, IaC, Kill Switch | 20 | `10.20.20.15` | `10.20.20.1` |

## Services hébergés sur Infra-services (`10.20.20.15`)

| Service | Accès | Rôle |
|---------|-------|------|
| Nginx | HTTPS | Reverse proxy (`netbox`, `vault`, `wazuh`, `api`.mar2.local) |
| Vault | `:8200` ou HTTPS proxy | Gestion des secrets (KV v2, AppRole) |
| NetBox | HTTPS | Documentation infrastructure |
| Terraform | local | Provisionnement Proxmox |
| Ansible | local | Configuration automatisée |
| Kill Switch | `:9000` | Blocage IP, isolation segment, coupure VPN |

> Les machines disposent d'une IP dédiée ; Vault, NetBox, Nginx, Terraform, Ansible et Kill Switch sont regroupés sur Infra-services et exposés par port ou reverse proxy.

---

# §4 — Réseau, routage et VPN

Les pfSense gèrent routage inter-VLAN, NAT, publications de services et VPN. Le tunnel **IPsec** transporte les réseaux inter-sites (production S1, security S2, backup, utilisateurs). **Pas de NAT** entre VLAN privés transportés par IPsec — visibilité des adresses sources pour la journalisation.

## Matrice de flux

| Flux | Source | Destination | Usage |
|------|--------|-------------|-------|
| IPsec | VLAN 10/30/40 Site 1 | VLAN 20/30/40 Site 2 | Transport chiffré inter-sites |
| OpenVPN SSL/TLS | Utilisateurs distants | pfSense-01 / VLAN 40 | VPN utilisateurs |
| LDAPS | OpenVPN / VLAN 40 | AD `10.10.10.100:636` | Authentification VPN sur AD |
| DNS / Kerberos / LDAP | VLAN 40 Utilisateurs | VLAN 10 Production | Auth, DNS, annuaire |
| Wazuh Agents | VLAN 10 Production | `10.20.20.13:1514/1515/55000` | Remontée événements |
| Bastion | Réseaux autorisés | Guacamole `10.20.20.14` | SSH/RDP centralisé |
| Apps / DB | VLAN 40 / services autorisés | `10.10.10.52` | Accès applicatif |
| Sauvegardes | VLAN 30 | Services critiques | NetBox, Vault, Wazuh, DB, configs |
| Internet | VLAN autorisés | WAN pfSense | Sortie NAT contrôlée |

```bash
ping -c 3 10.20.20.15
ping -c 3 10.10.10.100
traceroute 10.20.20.15
```

pfSense → VPN → IPsec → Status : tunnel **Established**.

---

# §5 — Règles de pare-feu

Politique **moindre privilège** : deny par défaut, règles du plus spécifique au plus général, **deny final journalisé**.

## WAN (les deux sites)

| Action | Source | Destination | Service | Objectif |
|--------|--------|-------------|---------|----------|
| Pass | IP WAN pair | WAN address | UDP 500/4500, ESP | IPsec site-à-site |
| Pass | Utilisateurs distants | WAN Site 1 | OpenVPN SSL/TLS | VPN + LDAPS |
| Block | RFC1918/Bogon | WAN address | Any | Anti-spoofing |
| Block + Log | Any | Any | Any | Deny final |

## LAN natif pfSense

| Action | Source | Destination | Objectif |
|--------|--------|-------------|----------|
| Block | LAN net | Any | Aucun usage machine sur LAN natif |
| Pass (optionnel) | Poste admin local | pfSense LAN HTTPS | Administration temporaire |
| Block + Log | Any | Any | Deny final |

## IPsec (inter-sites)

| Action | Source | Destination | Service | Objectif |
|--------|--------|-------------|---------|----------|
| Pass | VLAN 20 Security | AD `10.10.10.100` | DNS, Kerberos, LDAP/LDAPS | Auth AD |
| Pass | VLAN 10 Production | Wazuh `10.20.20.13` | 1514, 1515, 55000 | Agents Wazuh |
| Pass | VLAN 40 Users | Guacamole `10.20.20.14` | HTTPS | Accès bastion |
| Pass | VLAN 30 Backup | VLAN 30 distant | Ports sauvegarde | Backup inter-sites |
| Block + Log | Any | Any | Any | Flux non prévu |

## VLAN 10 — Production (Site 1)

| Action | Source | Destination | Service | Objectif |
|--------|--------|-------------|---------|----------|
| Pass | VLAN 10 | AD `10.10.10.100` | DNS, Kerberos, LDAP/LDAPS, SMB | Services domaine |
| Pass | VLAN 10 | Apps/DB `10.10.10.52` | Ports applicatifs, 3306 | Application et base |
| Pass | VLAN 10 | Wazuh `10.20.20.13` | 1514, 1515, 55000 | Supervision |
| Pass | VLAN 10 | Internet | HTTP/HTTPS, DNS, NTP | Mises à jour |
| Block + Log | VLAN 10 | Any | Any | Deny final |

## VLAN 20 — Security (Site 2)

| Action | Source | Destination | Service | Objectif |
|--------|--------|-------------|---------|----------|
| Pass | Wazuh | VLAN autorisés | Agent/API | Collecte |
| Pass | Guacamole | Serveurs autorisés | SSH/RDP | Administration bastion |
| Pass | Infra-services | AD `10.10.10.100` | LDAPS, DNS | Auth et résolution |
| Pass | Infra-services | Internet | HTTP/HTTPS, DNS, NTP | Mises à jour conteneurs |
| Block + Log | VLAN 20 | Any | Any | Deny final |

## VLAN 30 — Backup

| Action | Source | Destination | Objectif |
|--------|--------|-------------|----------|
| Pass | VLAN 30 S1 | AD, Apps/DB | Sauvegarde services métier |
| Pass | VLAN 30 S2 | Wazuh, Infra-services | Sauvegarde services sécurité |
| Pass | VLAN 30 | VLAN 30 distant | Réplication inter-sites |
| Block | VLAN 30 | Internet | Pas d'accès Internet direct |
| Block + Log | VLAN 30 | Any | Deny final |

## VLAN 40 — Utilisateurs

| Action | Source | Destination | Objectif |
|--------|--------|-------------|----------|
| Pass | VLAN 40 | AD, Apps/DB, Guacamole, Internet | Services autorisés |
| **Block** | VLAN 40 | **VLAN 20 Security** | Pas d'accès direct (sauf Guacamole) |
| Block | VLAN 40 | VLAN 30 Backup | Pas d'accès sauvegardes |
| Block + Log | VLAN 40 | Any | Deny final |

## OpenVPN SSL/TLS

| Action | Source | Destination | Objectif |
|--------|--------|-------------|----------|
| Pass | OpenVPN net | AD `10.10.10.100` | Auth et résolution |
| Pass | OpenVPN net | Apps/DB `10.10.10.52` | Accès utilisateur distant |
| Pass | OpenVPN net | Guacamole `10.20.20.14` | Accès bastion |
| Block | OpenVPN net | VLAN 20 Security | Pas d'accès direct sécurité |
| Block | OpenVPN net | VLAN 30 Backup | Pas d'accès sauvegardes |
| Block + Log | OpenVPN net | Any | Deny final |

---

# §6 — Services d'identité

| Élément | Détail |
|---------|--------|
| Domaine | `mar2.local` |
| DNS | Serveur AD/DNS `10.10.10.100` |
| Structure | Utilisateurs, groupes, OU |
| Flux | LDAP, LDAPS, Kerberos, DNS, SMB, RDP |
| DHCP | Scopes VLAN 40 ; IP fixes pour serveurs critiques |
| VPN utilisateurs | OpenVPN SSL/TLS S1 → authentification **LDAPS** sur AD |

```bash
nslookup mar2.local 10.10.10.100
nslookup netbox.mar2.local
nslookup vault.mar2.local
nslookup wazuh.mar2.local
```

---

# §7 — Sécurité périmétrique et accès

- **pfSense** × 2 : filtrage entrants, sortants, inter-sites
- **Guacamole** `10.20.20.14` : bastion SSH/RDP centralisé
- **Nginx** sur Infra-services : reverse proxy HTTPS
- **IPsec** site-à-site + accès client-à-site
- Pas d'exposition LAN directe depuis Internet

```bash
curl -Ik https://netbox.mar2.local
curl -Ik https://vault.mar2.local
# Sans VPN : services internes non joignables depuis Internet
```

Connexion bastion :

```bash
# Via Guacamole
https://10.20.20.14

# Ou SSH direct depuis réseau autorisé
ssh admin@10.20.20.14
```

---

# §8 — Supervision (Wazuh)

| Composant | Rôle |
|-----------|------|
| Wazuh Manager (`10.20.20.13`) | Réception, analyse, corrélation |
| Wazuh Indexer | Indexation et stockage |
| Wazuh Dashboard | Visualisation agents, alertes |
| Filebeat | Acheminement vers l'indexer |
| Agents | Collecte sur serveurs critiques (S1 + S2) |

```bash
ssh admin@10.20.20.14 "logger 'CIA-SOUTENANCE-TEST'"
```

Wazuh Dashboard → Discover → `CIA-SOUTENANCE-TEST` · alertes SSH · dashboards connexions.

---

# §9 — Vault

| Fonctionnalité | État |
|----------------|------|
| Stockage Raft intégré | ✅ |
| Moteur KV v2 (`infra/`) | ✅ |
| Policies moindre privilège | ✅ |
| AppRole Ansible | ✅ |
| Snapshots Raft automatiques | ✅ |
| Secrets hors Git | ✅ |
| **Authentification LDAP (AD)** | **🟡 En cours** |

Vault centralise mots de passe, tokens et clés — utilisé par Ansible via AppRole. **Seul point non finalisé :** branchement LDAP pour l'auth utilisateurs Vault sur `10.10.10.100`.

Accès : `https://vault.mar2.local` · `10.20.20.15:8200`

---

# §10 — NetBox

Référentiel technique : sites, équipements, préfixes, adresses IP, VLAN, services, matrice de flux.

`https://netbox.mar2.local` · sync inventaire via script Python et playbook Ansible.

---

# §11 — Automatisation (Ansible / Terraform)

| Outil | Usage | État |
|-------|-------|------|
| Terraform | Provisionnement VMs Proxmox (Cloud-Init) | ✅ |
| Ansible | Rôles, playbooks, orchestration post-déploiement | ✅ |
| Vault | Secrets pour l'automatisation (AppRole) | ✅ |
| NetBox | Référentiel des ressources créées | ✅ |

Chaîne : **Terraform** (création VM) → **Ansible** (configuration) → **Vault** (secrets) → **NetBox** (documentation).

```bash
cd iac/ansible && ansible-playbook playbooks/site.yml --syntax-check
cd iac/terraform && terraform validate && terraform plan
```

---

# §12 — Sauvegardes et PRA

| Composant | Méthode |
|-----------|---------|
| Vault | Snapshots Raft automatiques |
| NetBox / PostgreSQL | Sauvegarde planifiée |
| Wazuh | Éléments critiques indexés |
| pfSense | Export XML sanitisé |
| AD | Sauvegarde système |
| Apps/DB | Sauvegarde MariaDB |

## Ordre de reconstruction

```text
1. Proxmox S1/S2 (restore vzdump)
2. Réseau / VLAN
3. pfSense + config sanitisée
4. VPN IPsec (secrets depuis Vault)
5. AD mar2.local + DNS
6. Infra-services (Vault, NetBox, Wazuh, Nginx)
7. Guacamole
8. Tests : VPN, DNS, NetBox, Wazuh, Guacamole, Kill Switch
```

Scénarios PRA documentés : perte AD · perte Vault · perte VPN · perte serveur · perte site entier.

---

# §13 — Kill Switch

API sur `10.20.20.15:9000` (`api.mar2.local`) :

1. Identification événement de sécurité (Wazuh)
2. Déclenchement blocage IP / isolation segment / coupure VPN
3. Interaction pfSense, Proxmox ou Wazuh selon scénario
4. Traçabilité et retour arrière contrôlé (< 10 min)

```bash
curl -X POST https://api.mar2.local/kill-switch/status
# Coupure VPN de test : pfSense S2 → IPsec → disable Phase 1 → ping 10.20.20.15 échoue → réactiver
```

---

# §14 — Diagrammes

| Livrable | Fichier |
|----------|---------|
| Schéma PNG | [architecture-diagram.png](./architecture-diagram.png) |
| Source Mermaid | [architecture-diagram.mmd](./architecture-diagram.mmd) |
| Matrice de flux complète | Document technique §4–5 |

```bash
npx @mermaid-js/mermaid-cli -i docs/architecture-diagram.mmd -o docs/architecture-diagram.png
```

---

# §15 — Dépôt Git et équipe

| Membre | Domaines |
|--------|----------|
| **Meriem ZAHZOUH** | Architecture, réseau S2, pfSense, Guacamole, document technique, démonstration |
| **Kévin SEMERCIYAN** | Infra-services, Vault, Wazuh, Ansible, Terraform, NetBox, PRA |
| **Fabio TILLET** | Équipe projet |
| **Équipe** | Revue, captures, soutenance |

Dépôt : document technique, guides Markdown, configs sanitisées, IaC, scripts — branches `feature/`, commits conventionnels, aucun secret versionné.

---

# §16 — Démonstration technique

| Étape | Preuve |
|-------|--------|
| Proxmox | VMs sur S1 (`192.168.156.11`) et S2 (`192.168.102.11`) |
| IPsec | Communication entre VLAN autorisés S1 ↔ S2 |
| OpenVPN | Connexion utilisateur + LDAPS AD |
| Wazuh | Agents actifs, manager/indexer/dashboard |
| Vault | Initialisé, AppRole Ansible opérationnel |
| NetBox | Sites, VLAN, IP, équipements référencés |
| Guacamole | Connexion SSH/RDP centralisée |
| Ansible/Terraform | Provisionnement + configuration |
| Kill Switch | Coupure et restauration VPN |
| Pare-feu | Moindre privilège, deny final journalisé |

## Commandes

```bash
ping -c 2 10.20.20.15
ping -c 2 10.10.10.100
curl -Ik https://netbox.mar2.local
curl -Ik https://vault.mar2.local
curl -Ik https://wazuh.mar2.local
nslookup netbox.mar2.local 10.10.10.100
ssh admin@10.20.20.14 "logger 'CIA-SOUTENANCE-TEST'"
cd iac/terraform && terraform plan
```

---

# Synthèse des 29 trophées

| Trophée | État | Remarque |
|---------|------|----------|
| `infra_delivery` | ✅ | Infra hybride opérationnelle |
| `infra_spec` | ✅ | VLAN, IP, rôles documentés |
| `infra_scalability` | ✅ | Modèle site N (convention VLAN) |
| `infra_choices` | ✅ | Stack open source justifiée |
| `diagram_delivery` | ✅ | PNG + Mermaid + docx |
| `diagram_quality` | ✅ | 2 sites, VLAN, flux IPsec |
| `iac_delivery` | ✅ | Ansible + Terraform |
| `iac_quality` | ✅ | Modulaire, secrets via Vault |
| `network_spec1` | ✅ | Site 1 production + AD |
| `network_spec2` | ✅ | Site 2 security + services |
| `network_vpn` | ✅ | IPsec + OpenVPN LDAPS |
| `network_firewall` | ✅ | Règles VLAN + deny log |
| `network_dns` | ✅ | mar2.local, zones internes |
| `network_ip_mngmt` | ✅ | NetBox référentiel |
| `sec_access` | ✅ | Nginx HTTPS, pas d'expo LAN |
| `sec_bastion` | ✅ | Guacamole centralisé |
| `sec_credentials` | 🟡 | Vault OK — **LDAP en cours** |
| `incident_killswitch` | ✅ | API + coupure VPN < 10 min |
| `incident_recovery` | ✅ | PRA documenté et testé |
| `log_centralisation` | ✅ | Wazuh manager + agents |
| `log_observability` | ✅ | Événements centralisés |
| `log_analysis` | ✅ | Alertes SSH, filtres |
| `log_visuals` | ✅ | Dashboards Wazuh |
| `repo_practices` | ✅ | Workflow Git |
| `repo_doc` | ✅ | Document technique + guides |
| `repo_content` | ✅ | configs + iac + apps |
| `proj_subdivision` | ✅ | Meriem / Kévin / Fabio |
| `proj_planning` | ✅ | 100 % |
| `proj_presentation` | ✅ | Ce document |

---

## Conclusion

L'infrastructure **T-NSA-810-CIA** combine virtualisation, sécurité réseau, identité, supervision, bastion, gestion des secrets, documentation et automatisation. Deux sites, IPsec, segmentation VLAN, services de sécurité centralisés sur le Site 2 — architecture cohérente et représentative d'un environnement d'entreprise.

**Protéger · Superviser · Administrer · Documenter · Restaurer**

---

## Références

| Fichier | Contenu |
|---------|---------|
| [T-NSA-810-CIA_Document_technique_infrastructure (2).docx](./T-NSA-810-CIA_Document_technique_infrastructure%20(2).docx) | Document technique complet |
| [trophees-validation.md](./trophees-validation.md) | Index 29 trophées |
| [drp-runbook.md](./drp-runbook.md) | PRA et Kill Switch |
| [team-subdivision.md](./team-subdivision.md) | Répartition équipe |
