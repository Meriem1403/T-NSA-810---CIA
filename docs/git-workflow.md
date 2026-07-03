# Flux Git — pratiques de dépôt (`repo_practices`)

## Branches

| Branche | Usage |
|---------|-------|
| `main` | État présentable, doc alignée infra réelle, soutenance |
| `feature/<sujet>` | Périmètre limité : VPN, bastion, NetBox, terraform… |
| `fix/<sujet>` | Correctifs playbook, docs, scripts |

## Commits

Forme impérative (français ou anglais) :

```text
feat(vpn): documente tunnel IPsec site-à-site
docs(trophees): ajoute guide validation 29 trophées
fix(ansible): handler restart nginx bastion
iac(terraform): ajoute module VM Cloud-Init Proxmox
```

## Pull Requests

- Description claire du changement
- Liste des **tests manuels** effectués avant merge
- Vérification : aucun secret dans le diff
- Revue par un autre membre de l'équipe

## Interdictions (`.gitignore`)

```text
*.ovpn, *.pem, *.key, .env
inventory/production.yml, vault.yml
*.tfstate, terraform.tfvars
secrets/
```

## Contenu attendu (`repo_content`)

| Dossier | Contenu |
|---------|---------|
| `docs/` | 20+ fichiers documentation |
| `configs/` | pfSense, DNS, NetBox, Wazuh |
| `iac/` | Ansible, Terraform, Docker |
| `apps/` | Site interne |
| `scripts/` | Kill switch |
| `legacy/` | Archive Flux/K8s |

## Trophées dépôt couverts

- `repo_practices` — ce fichier + historique Git propre
- `repo_doc` — README + index `trophees-validation.md`
- `repo_content` — arborescence complète versionnée

## Références

- [`trophees-validation.md`](./trophees-validation.md)
- [`team-subdivision.md`](./team-subdivision.md)
