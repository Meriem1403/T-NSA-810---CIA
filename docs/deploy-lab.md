# Déploiement labo — InfraService, NetBox, Vault, Wazuh, Terraform

Guide pas à pas aligné sur l’état du labo au **23 juin 2026** ([`status-2026-06-23.md`](./status-2026-06-23.md)).

## Prérequis

- VPN IPsec connecté (accès `192.168.10.0/24` et réseaux S1 si routés).
- Hôte **`infraservice`** : `192.168.10.15` (NetBox, Vault, Wazuh, Ansible, Terraform).
- Accès SSH à `infraservice` depuis le bastion ou le VPN.
- Secrets dans **HashiCorp Vault** ou fichier local `iac/ansible/vault.yml` (non Git).

## 1. Vérifier les services sur InfraService

```bash
ssh user@192.168.10.15

# NetBox
curl -I http://192.168.10.15:8000/

# Vault (si déverrouillé)
curl http://192.168.10.15:8200/v1/sys/health

# Docker (NetBox, PostgreSQL, Valkey)
docker ps
```

## 2. NetBox — token API et synchronisation IPAM

1. UI NetBox → Admin → API tokens → Create.
2. Stocker le token dans Vault (`infra/netbox`) ou coffre d’équipe.
3. Lancer la sync :

```bash
export NETBOX_URL=http://192.168.10.15:8000
export NETBOX_TOKEN=<depuis Vault>
python3 configs/netbox/scripts/sync_from_inventory.py
```

Ou via Ansible :

```bash
cd iac/ansible
cp inventory/example.inventory.yml inventory/production.yml
ansible-playbook -i inventory/production.yml playbooks/netbox-sync.yml -e @vault.yml
```

## 3. Ansible — baseline et bastion

```bash
cd iac/ansible
ansible-playbook -i inventory/production.yml playbooks/site.yml
```

Rôle `bastion` : déploie nginx + site interne sur `192.168.10.11`.

## 4. Vault — intégration Ansible (AppRole)

1. Vérifier le moteur KV `infra/` et la policy Ansible.
2. Configurer AppRole (Secret ID hors Git).
3. Tester la lecture d’un secret :

```bash
ansible-playbook -i inventory/production.yml playbooks/site.yml --tags common --check
```

Voir [`secrets-and-access.md`](./secrets-and-access.md).

## 5. Wazuh — agents et dashboards

1. Vérifier le manager Wazuh sur `infraservice`.
2. Confirmer les agents sur bastion et hôtes supervisés.
3. Générer un événement test :

```bash
ssh -p 2222 bastion@78.202.114.212 "logger 'CIA-WAZUH-TEST'"
```

4. Vérifier l’événement dans l’interface Wazuh (< 2 min).
5. Finaliser dashboards et alertes pour la soutenance.

> **Legacy :** le playbook `deploy-observability.yml` (Filebeat → Elastic) reste disponible pour référence ; la supervision courante utilise Wazuh.

## 6. Terraform — provisionnement VM

```bash
cd iac/terraform
terraform init
terraform validate
terraform plan
```

**Blocage actuel :** créer le template Cloud-Init `ubuntu-template` sur Proxmox, puis :

```bash
terraform apply
```

Enchaîner avec Ansible sur la VM créée.

## 7. Kill switch (< 10 min)

Chronomètre + captures écran.

```bash
./scripts/kill-switch-s2.sh status
```

1. pfSense S2 → **VPN > IPsec** — désactiver tunnel ou règle WAN associée → **Apply**.
2. Client VPN : `ping 192.168.10.15` doit **échouer**.
3. Réactiver → **Apply** → ping OK.
4. Documenter horodatage dans [`drp-runbook.md`](./drp-runbook.md).

## 8. HTTPS et LDAPS (à finaliser)

1. Finaliser la PKI Active Directory `mar2.local`.
2. Déployer Nginx reverse proxy sur `infraservice`.
3. Activer HTTPS pour NetBox, Vault, Wazuh, Guacamole.
4. Configurer LDAP/LDAPS dans NetBox et Vault.

## 9. Sauvegardes

| Composant | Méthode | État |
|-----------|---------|------|
| Vault | Snapshots Raft automatiques | ✅ |
| NetBox / PostgreSQL | À industrialiser | 🟡 |
| pfSense | Export config sanitisé | Manuel |

Tester une restauration complète avant la soutenance.

## 10. Dépannage

| Problème | Action |
|----------|--------|
| NetBox 502 | `docker compose logs -f netbox` sur infraservice |
| Vault sealed | Procédure unseal (clés hors Git) |
| Agent Wazuh absent | `systemctl status wazuh-agent`, firewall LAN |
| Terraform plan échoue | Vérifier template `ubuntu-template` et credentials API Proxmox |
| Ansible + Vault | Vérifier AppRole, `community.hashi_vault`, URL Vault |

## 11. Diagramme soutenance

Régénérer si besoin :

```bash
npx @mermaid-js/mermaid-cli -i docs/architecture-diagram.mmd -o docs/architecture-diagram.png
```

Fichier livré : [`architecture-diagram.png`](./architecture-diagram.png).
