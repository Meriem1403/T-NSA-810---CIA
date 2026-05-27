# Terraform (optionnel)

Si vous utilisez un provider **Proxmox** (ou autres), placez vos modules ici.

Règles :

- **`terraform.tfvars`** et fichiers d’état (**`*.tfstate`**) hors Git ou backend distant sécurisé.
- Versions providers épinglées dans `versions.tf`.

Exemple d’entrée après `terraform init` :

```bash
cd iac/terraform
terraform fmt -recursive
terraform validate
```
