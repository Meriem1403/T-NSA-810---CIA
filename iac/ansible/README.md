# Ansible — infrastructure CIA

Automatiser : bastion (nginx site interne, SSH), synchronisation NetBox, agents Filebeat (à venir).

## Playbooks

| Fichier | Description |
|---------|-------------|
| `playbooks/site.yml` | Baseline + rôle `bastion` |
| `playbooks/netbox-sync.yml` | Sync IPAM via API (dry-run par défaut) |

## Utilisation rapide

```bash
cd iac/ansible
cp inventory/example.inventory.yml inventory/production.yml

ansible-playbook -i inventory/production.yml playbooks/site.yml --check
ansible-playbook -i inventory/production.yml playbooks/site.yml --limit site2_bastion

export NETBOX_URL=https://netbox.example.local NETBOX_TOKEN=...
ansible-playbook playbooks/netbox-sync.yml -e netbox_sync_dry_run=false
```

## Rôles

- `common` — connectivité et inventaire
- `bastion` — site interne + durcissement SSH
- `netbox_sync` — script `configs/netbox/scripts/sync_from_inventory.py`

## Secrets

Variables via environnement ou `ansible-vault` — jamais de token en clair dans Git.
