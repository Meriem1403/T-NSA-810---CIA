# NetBox — IPAM

Instance labo : `http://192.168.10.15:8000` (hôte `infraservice`).

- Scripts Python appelant l’API avec **token en variable d’environnement** ou Vault (`infra/netbox`).
- Modèles de préfixes / sites : [`sites-prefixes.example.yml`](./sites-prefixes.example.yml).
- Sync : [`scripts/sync_from_inventory.py`](./scripts/sync_from_inventory.py).
- Playbook Ansible : `iac/ansible/playbooks/netbox-sync.yml`.

```bash
export NETBOX_URL=http://192.168.10.15:8000
export NETBOX_TOKEN=<depuis Vault>
python3 configs/netbox/scripts/sync_from_inventory.py --dry-run
```

**Reste à faire :** compléter l’inventaire NetBox (sites, VLAN, équipements, VMs) pour la soutenance.
