# Ansible — infrastructure CIA

## Playbooks

| Fichier | Description |
|---------|-------------|
| `playbooks/site.yml` | Baseline + bastion S2 (nginx, SSH) |
| `playbooks/deploy-site1.yml` | Docker + NetBox + Elastic sur `svc-s1` |
| `playbooks/deploy-observability.yml` | Filebeat bastion → Elastic S1 |
| `playbooks/netbox-sync.yml` | Sync IPAM API |

## Déploiement complet

Voir [`../../docs/deploy-lab.md`](../../docs/deploy-lab.md).

```bash
cd iac/ansible
cp inventory/example.inventory.yml inventory/production.yml
# Créer vault.yml avec mots de passe (hors Git)

ansible-playbook -i inventory/production.yml playbooks/deploy-site1.yml -e @vault.yml
export NETBOX_URL=http://192.168.199.20:8080 NETBOX_TOKEN=...
ansible-playbook playbooks/netbox-sync.yml -e netbox_sync_dry_run=false -e @vault.yml

ansible-playbook -i inventory/production.yml playbooks/deploy-observability.yml -e @vault.yml
```

## Rôles

| Rôle | Cible |
|------|-------|
| `docker_host` | Installation Docker CE |
| `netbox_stack` | Compose NetBox |
| `elastic_stack` | Compose ES + Kibana |
| `filebeat` | Agent logs bastion S2 |
| `bastion` | Site interne nginx |
| `netbox_sync` | Script API préfixes |

## Secrets

`vault.yml` (gitignored) ou variables `vault_*` — jamais en clair dans Git.
