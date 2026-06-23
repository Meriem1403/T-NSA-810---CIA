# Planification — phases CIA

Dernière mise à jour : **2026-06-23**

## Avancement global

**Avancement estimé du projet : 90 %**

L’infrastructure réseau, la virtualisation, les VPN, les services d’administration et la gestion des secrets sont largement opérationnels. Les travaux restants concernent principalement la finalisation de Terraform, HTTPS/PKI, LDAPS, le Kill Switch, les sauvegardes NetBox/PostgreSQL, les dashboards Wazuh et la préparation de la soutenance.

## Avancement par phase

| Phase | Jalons | Avancement | Statut |
|-------|--------|-----------:|--------|
| F0 — Bootstrap | Dépôt Git, README, workflow Git, `.gitignore` | 100 % | ✅ Terminé |
| F1 — Cadrage et architecture | Diagramme, backlog, grille d’évaluation, conventions d’adressage | 100 % | ✅ Terminé |
| F2 — Fondations Proxmox | Deux nœuds Proxmox, réseaux, stockages et VMs principales | 100 % | ✅ Terminé |
| F3 — Sécurité réseau | Deux pfSense, règles principales, NAT, segmentation | 100 % | ✅ Terminé |
| F4 — VPN | VPN site-à-site IPsec et VPN client-à-site | 100 % | ✅ Terminé |
| F5 — Identité et accès | AD `mar2.local`, DNS, Guacamole, bastion | 85 % | 🟡 LDAPS, PKI et durcissement à finaliser |
| F6 — Supervision | Wazuh, agents, collecte des événements | 80 % | 🟡 Dashboards, alertes et preuves à finaliser |
| F7 — Services InfraService | Docker, NetBox, PostgreSQL, Valkey, Vault | 95 % | 🟢 Fonctionnel, sauvegardes NetBox/PostgreSQL à finaliser |
| F8 — Automatisation Ansible | Inventaire, playbooks, intégration Vault AppRole | 100 % | ✅ Terminé |
| F9 — Infrastructure as Code Terraform | Installation, provider Proxmox, `init`, `validate`, `plan` | 70 % | 🟡 Template Cloud-Init et `apply` final à réaliser |
| F10 — Kill Switch et reprise | Scripts/API d’isolement, procédure de retour arrière, restauration | 40 % | 🟡 Développement et tests chronométrés à terminer |
| F11 — Documentation et soutenance | Documentation, captures, démonstration, supports | 75 % | 🟡 Gantt, preuves et slides à finaliser |

## Jalons validés

- Deux hyperviseurs Proxmox configurés.
- Deux pare-feu pfSense configurés.
- VPN site-à-site opérationnel.
- VPN client-à-site opérationnel.
- Active Directory et DNS du domaine `mar2.local` opérationnels.
- Guacamole déployé et fonctionnel.
- Wazuh déployé avec agents.
- NetBox déployé en Docker sur `192.168.10.15:8000`.
- PostgreSQL et Valkey fonctionnels.
- Vault opérationnel avec Raft, KV v2, policies, AppRole et snapshots.
- Ansible opérationnel avec lecture des secrets Vault validée.
- Terraform installé et connecté à l’API Proxmox.
- `terraform init`, `terraform validate` et `terraform plan` validés.
- Documentation d’état ajoutée dans `docs/status-2026-06-23.md`.

## Backlog restant priorisé

| Priorité | Action | Critère d’évaluation associé | État |
|---------:|--------|------------------------------|------|
| 1 | Créer un template Ubuntu Cloud-Init sur Proxmox | IaC / livraison de l’infrastructure | 🔴 À faire |
| 2 | Finaliser `terraform apply` pour déployer une VM de test | IaC / qualité IaC | 🔴 À faire |
| 3 | Enchaîner Terraform puis Ansible pour la configuration post-déploiement | IaC / reproductibilité | 🟡 À finaliser |
| 4 | Mettre en place HTTPS pour NetBox, Vault, Wazuh et Guacamole | Sécurité / moindre privilège | 🟡 À finaliser |
| 5 | Finaliser la PKI et LDAPS du domaine `mar2.local` | Identité / sécurité des accès | 🟡 À finaliser |
| 6 | Configurer LDAP/LDAPS dans NetBox et Vault | Gestion des identifiants | 🟡 À finaliser |
| 7 | Finaliser le Kill Switch : blocage IP, isolation VM, coupure VPN/VLAN | Gestion d’incident | 🔴 À faire |
| 8 | Relier Wazuh au Kill Switch | Supervision / réponse à incident | 🔴 À faire |
| 9 | Automatiser les sauvegardes NetBox et PostgreSQL | Reprise après sinistre | 🟡 À finaliser |
| 10 | Tester une restauration complète et chronométrée | DRP / reproductibilité | 🔴 À faire |
| 11 | Finaliser les dashboards et alertes Wazuh | Observabilité / analyse des journaux | 🟡 À finaliser |
| 12 | Compléter NetBox avec les sites, VLAN, préfixes, équipements et VMs | IPAM automatisé | 🟡 À finaliser |
| 13 | Affecter les tâches restantes aux membres de l’équipe | Planification / backlog | 🟡 À finaliser |
| 14 | Préparer les captures, slides et scénario de démonstration | Présentation professionnelle | 🔴 À faire |

## Plan d’action recommandé

### Étape 1 — Finalisation IaC

1. Créer le template Ubuntu Cloud-Init.
2. Corriger la ressource Terraform si nécessaire.
3. Exécuter `terraform plan`.
4. Exécuter `terraform apply`.
5. Vérifier la VM dans Proxmox.
6. Lancer Ansible sur la VM créée.

### Étape 2 — Sécurité et identité

1. Finaliser la PKI AD.
2. Activer HTTPS sur les services internes.
3. Déployer les certificats.
4. Configurer LDAPS pour NetBox et Vault.
5. Faire tourner les identifiants et secrets exposés pendant les tests.

### Étape 3 — Supervision et incident

1. Finaliser les dashboards Wazuh.
2. Créer des scénarios d’alerte.
3. Développer les actions du Kill Switch.
4. Tester l’isolation et le retour arrière.
5. Capturer les preuves pour la soutenance.

### Étape 4 — Sauvegarde et reprise

1. Automatiser les sauvegardes NetBox/PostgreSQL.
2. Vérifier les snapshots Vault.
3. Documenter les commandes de restauration.
4. Réaliser un test complet de reconstruction.
5. Mesurer et documenter le temps de reprise.

### Étape 5 — Soutenance

1. Mettre à jour le diagramme d’architecture.
2. Finaliser le support de présentation.
3. Préparer les commandes de démonstration.
4. Joindre les captures de preuves.
5. Réaliser une répétition chronométrée.

## Journal des décisions

| Date | Décision |
|------|----------|
| 2026-05-29 | NetBox et Elastic initialement prévus sur une VM Docker dédiée. |
| 2026-06-01 | Remplacement progressif de la supervision ELK par Wazuh. |
| 2026-06-21 | Reconstruction de NetBox, Vault et Ansible sur l’hôte InfraService. |
| 2026-06-23 | Validation de l’intégration Ansible ↔ Vault par AppRole. |
| 2026-06-23 | Installation de Terraform et validation du provider Proxmox. |
| 2026-06-23 | Blocage Terraform identifié : absence du template `ubuntu-template`. |
| 2026-06-23 | Avancement global réévalué à 90 % selon la grille d’évaluation mise à jour. |

## Indicateurs de fin de projet

Le projet pourra être considéré à 100 % lorsque les conditions suivantes seront remplies :

- une VM est créée avec Terraform ;
- sa configuration est finalisée avec Ansible ;
- HTTPS et LDAPS sont actifs ;
- le Kill Switch est testé et réversible ;
- les sauvegardes NetBox/PostgreSQL sont automatisées et restaurables ;
- les dashboards et alertes Wazuh sont finalisés ;
- les objets NetBox sont complets ;
- les preuves, slides et démonstrations sont prêtes.
