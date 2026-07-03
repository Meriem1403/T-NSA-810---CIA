# Terraform — provisionnement Proxmox

Dernière mise à jour : **23 juin 2026**.

## État actuel

| Étape | Statut |
|-------|--------|
| Installation Terraform | ✅ |
| Provider `telmate/proxmox` (`terraform init`) | ✅ |
| `terraform validate` | ✅ |
| `terraform plan` | ✅ |
| `terraform apply` | 🟡 Bloqué — template `ubuntu-template` manquant sur Proxmox |

## Prérequis

- Accès API Proxmox (credentials dans Vault `infra/proxmox`, hors Git).
- Template **Ubuntu Cloud-Init** nommé `ubuntu-template` sur chaque nœud cible.
- Backend d’état distant ou `.tfstate` **hors Git**.

## Utilisation

```bash
cd iac/terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan
# terraform apply   # après création du template
```

## Chaîne cible

1. **Terraform** : création VM (ressources, disque, réseau, cloud-init).
2. **Ansible** : configuration post-déploiement (rôles, services, agents Wazuh).

Voir [`../../docs/deploy-lab.md`](../../docs/deploy-lab.md) section 6 et [`../../docs/gantt.md`](../../docs/gantt.md).

## Règles

- **`terraform.tfvars`** et **`*.tfstate`** hors Git ou backend distant sécurisé.
- Versions providers épinglées dans `versions.tf` (à ajouter lors de l’implémentation des modules).
