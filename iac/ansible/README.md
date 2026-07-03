# Ansible — infrastructure CIA

Dernière mise à jour : **23 juin 2026**.

## Playbooks

| Fichier | Description |
|---------|-------------|
| `playbooks/site.yml` | Baseline + bastion S2 (nginx, SSH) |
| `playbooks/deploy-site1.yml` | Docker + NetBox + Elastic sur hôte services (legacy ELK — voir note) |
| `playbooks/deploy-observability.yml` | Filebeat bastion → Elastic (legacy — Wazuh en prod labo) |
| `playbooks/netbox-sync.yml` | Sync IPAM via API NetBox |

## Hôte cible principal

**`infraservice`** — `192.168.10.15` : NetBox, Vault, Wazuh, Ansible, Terraform.

## Déploiement

Voir [`../../docs/deploy-lab.md`](../../docs/deploy-lab.md).

```bash
cd iac/ansible
cp inventory/example.inventory.yml inventory/production.yml

# Secrets : vault.yml local OU HashiCorp Vault AppRole
ansible-playbook -i inventory/production.yml playbooks/site.yml

export NETBOX_URL=http://192.168.10.15:8000 NETBOX_TOKEN=...
ansible-playbook -i inventory/production.yml playbooks/netbox-sync.yml -e @vault.yml
```

## Rôles

| Rôle | Cible | Statut |
|------|-------|--------|
| `docker_host` | Installation Docker CE | Actif |
| `netbox_stack` | Compose NetBox | Actif (sur infraservice) |
| `elastic_stack` | Compose ES + Kibana | Legacy |
| `filebeat` | Agent logs bastion S2 | Legacy (Wazuh agents en prod) |
| `bastion` | Site interne nginx | Actif |
| `netbox_sync` | Script API préfixes | Actif |

## Secrets

- **HashiCorp Vault** (recommandé) : AppRole Ansible, KV `infra/`
- **Fallback** : `vault.yml` (gitignored) avec variables `vault_*`

Jamais de secrets en clair dans Git.
