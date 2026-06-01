# Déploiement labo — NetBox, Elastic, Filebeat, kill switch

Guide pas à pas pour finaliser les critères restants sur l’infrastructure réelle.

## Prérequis

- VPN connecté vers site S2 (accès `192.168.102.0/24` et `192.168.199.0/24` si routé).
- VM **svc-s1** Ubuntu sur site 1 : `192.168.199.20` (2 vCPU, 4 Go RAM, 40 Go disque).
- Ansible installé sur votre poste : `pip install ansible`.
- Secrets dans un fichier local (non Git) : `iac/ansible/vault.yml` ou variables d’environnement.

## 1. Site 1 — VM services (NetBox + Elastic)

### Créer la VM sur Proxmox S1

1. **Create VM** → Ubuntu Server 24.04, 2 vCPU / 4 Go RAM / 40 Go.
2. IP statique : `192.168.199.20/24`, passerelle `192.168.199.1`.
3. Utilisateur `ubuntu`, SSH + clé ou mot de passe.

### Déployer avec Ansible

```bash
cd iac/ansible
cp inventory/example.inventory.yml inventory/production.yml
# Éditer ansible_user / clés SSH si besoin

# Secrets (exemple)
cat > vault.yml <<'EOF'
vault_netbox_db_password: "..."
vault_netbox_secret_key: "...(50+ caractères)..."
vault_netbox_superuser_password: "..."
vault_elastic_password: "..."
EOF

ansible-playbook -i inventory/production.yml playbooks/deploy-site1.yml -e @vault.yml
```

### Vérifications

```bash
curl -I http://192.168.199.20:8080/
curl -u elastic:MOT_DE_PASSE http://192.168.199.20:9200/_cluster/health
# Kibana : http://192.168.199.20:5601
```

### NetBox — token API

1. UI NetBox → Admin → API tokens → Create.
2. Exporter :

```bash
export NETBOX_URL=http://192.168.199.20:8080
export NETBOX_TOKEN=...
python3 configs/netbox/scripts/sync_from_inventory.py
```

## 2. Filebeat sur bastion S2

```bash
ansible-playbook -i inventory/production.yml playbooks/deploy-observability.yml -e @vault.yml
```

Générer un événement :

```bash
ssh -p 2222 bastion@78.202.114.212 "sudo logger 'CIA test log centralisation'"
```

Kibana → Discover → filtre `site: site2`.

## 3. Kill switch (< 10 min)

Chronomètre + captures écran.

```bash
./scripts/kill-switch-s2.sh status   # avant
```

1. pfSense S2 → **Firewall > Rules > WAN** → désactiver **UDP 1194** → **Apply**.
2. Client VPN : `ping 192.168.102.11` doit **échouer**.
3. `./scripts/kill-switch-s2.sh status`
4. Réactiver la règle → **Apply** → ping OK.

Documenter dans `docs/drp-runbook.md` (horodatage + captures).

## 4. Diagramme soutenance

Fichier livré : [`architecture-diagram.png`](./architecture-diagram.png) (généré depuis `.mmd`).

## 5. Dépannage

| Problème | Action |
|----------|--------|
| Elastic OOM | Augmenter RAM VM ou `ES_JAVA_OPTS=-Xms1g -Xmx1g` |
| NetBox 502 | `docker compose logs -f netbox` sur svc-s1 |
| Filebeat pas de logs | `systemctl status filebeat`, mot de passe elastic, firewall S1:9200 depuis 10.0/24 VPN |
