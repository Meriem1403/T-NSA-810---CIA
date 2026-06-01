# Secrets, identifiants et moindre privilège

## Principes

- Aucun mot de passe, clé privée ou token API dans Git (voir `.gitignore`).
- Coffre d’équipe (Bitwarden, 1Password, KeePass…) pour tous les secrets opérationnels.
- Comptes **dédiés** par fonction (bastion, NetBox API, Elastic, Proxmox).

## Matrice d’accès (résumé)

| Système | Compte type | Accès depuis | Stockage secret |
|---------|-------------|--------------|-----------------|
| Proxmox S2 | `Meriem` (admin labo) | VPN → `192.168.102.11:8006` | Coffre |
| pfSense | `admin` | LAN / VPN → `192.168.10.1` | Coffre |
| Bastion S2 | `bastion` | SSH `2222` public ou VPN | Coffre + clé SSH optionnelle |
| NetBox | token API lecture/écriture | LAN S1 | `NETBOX_TOKEN` env |
| Elastic | `elastic` / beats | LAN S1 | `ELASTIC_PASSWORD` env |
| OpenVPN | certificats client | Fichiers `.ovpn` **hors Git** | Coffre |

## Moindre privilège

- **Internet → LAN** : interdit sauf flux documentés (VPN, NAT bastion).
- **Bastion** : utilisateur sans besoin root quotidien ; `sudo` pour maintenance.
- **pfSense** : compte admin réservé aux changements firewall ; pas de partage compte soutenance.
- **NetBox** : token limité aux scopes `ipam.*` nécessaires au script de sync.

## Rotation et incident

1. Révoquer token / mot de passe compromis dans le coffre.
2. Régénérer clés OpenVPN si fuite `.ovpn`.
3. Consulter logs bastion + Elastic (quand déployé).
4. Kill switch réseau si exposition critique : [`drp-runbook.md`](./drp-runbook.md).

## Fichiers locaux non versionnés

```text
iac/ansible/inventory/production.yml
*.ovpn
.env
secrets/
```

Copier `inventory/example.inventory.yml` vers `production.yml` et renseigner les hôtes réels.
