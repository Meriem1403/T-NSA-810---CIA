# Ansible — infrastructure CIA

Automatiser : état VMs / paquets (`openvpn`, agents Filebeat…), désync inventaire ↔ NetBox, sauf exports sensibles hors Git.

## Utilisation rapide

```bash
cd iac/ansible
ansible-playbook playbooks/site.yml --check  # utilise inventory/example.inventory.yml par défaut

# Déploiement avec inventaire local non versionné :
ansible-playbook -i inventory/production.yml playbooks/site.yml
```

Ajoutez vos rôles dans `roles/` (ex. `roles/openvpn`, `roles/netbox-sync`).

## Secrets

`-e @vault.yml` avec fichiers `ansible-vault encrypt` uniquement hors dépôt ou chiffrés dans Git suivant politique enseignant.
