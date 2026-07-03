# Secrets, identifiants et moindre privilège

Dernière mise à jour : **23 juin 2026**.

## Principes

- Aucun mot de passe, clé privée, token API, PSK IPsec ou clé d’unseal Vault dans Git (voir `.gitignore`).
- **HashiCorp Vault** (`192.168.10.15:8200`) : source de vérité pour les secrets d’infrastructure (KV v2 `infra/`).
- Coffre d’équipe (Bitwarden, 1Password…) en complément pour accès humains.
- Comptes **dédiés** par fonction (bastion, NetBox API, Vault AppRole, Proxmox, AD).

## Matrice d’accès (résumé)

| Système | Compte type | Accès depuis | Stockage secret |
|---------|-------------|--------------|-----------------|
| Proxmox S1/S2 | admin labo | VPN → `:8006` | Vault `infra/proxmox` + coffre |
| pfSense | `admin` | LAN / VPN → `192.168.10.1` | Coffre |
| Bastion S2 | `bastion` | SSH `2222` public ou VPN | Coffre + clé SSH optionnelle |
| Guacamole | utilisateur dédié | LAN / VPN | Coffre |
| Active Directory | comptes de service | LAN S1 | AD + futur LDAPS |
| NetBox | token API | LAN → `192.168.10.15:8000` | Vault `infra/netbox` |
| Vault | `elastic` / admin | LAN → `:8200` | Clés unseal hors Git (shamir) |
| Ansible | AppRole | localhost sur infraservice | Vault AppRole (Secret ID hors Git) |
| Wazuh | admin / agents | LAN / VPN | Coffre |
| IPsec | PSK / certificats | pfSense GUI | Vault ou coffre (jamais Git) |

## Moindre privilège

- **Internet → LAN** : interdit sauf flux documentés (IPsec, NAT bastion 2222).
- **Bastion** : utilisateur sans root quotidien ; `sudo` pour maintenance.
- **pfSense** : compte admin réservé aux changements firewall.
- **NetBox** : token limité aux scopes `ipam.*` nécessaires au script de sync.
- **Vault** : policies par service ; AppRole Ansible en lecture seule sur `infra/*`.
- **AD** : comptes de service distincts pour NetBox, Vault (LDAPS à finaliser).

## Intégration Ansible ↔ Vault

- Collection : `community.hashi_vault`
- Authentification : **AppRole** (role_id versionné si besoin, secret_id **jamais** dans Git)
- Variables sensibles : préfixe `vault_*` ou lookup Vault dans les playbooks

## Rotation et incident

1. Révoquer token / mot de passe compromis dans Vault et le coffre.
2. Régénérer PSK IPsec ou certificats si fuite.
3. Consulter alertes **Wazuh** (connexions SSH, scans, échecs auth).
4. Kill switch réseau si exposition critique : [`drp-runbook.md`](./drp-runbook.md).
5. Rotation des identifiants exposés pendant les tests de labo.

## Fichiers locaux non versionnés

```text
iac/ansible/inventory/production.yml
iac/ansible/vault.yml
*.ovpn
.env
secrets/
*.tfstate
*.tfstate.backup
```

Copier `inventory/example.inventory.yml` vers `production.yml` et renseigner les hôtes réels.

## Sécurité documentaire

Aucun mot de passe, token, AppRole Secret ID, clé d’unseal, fichier d’état Terraform ou secret d’API ne doit être versionné dans Git (cf. [`status-2026-06-23.md`](./status-2026-06-23.md)).
