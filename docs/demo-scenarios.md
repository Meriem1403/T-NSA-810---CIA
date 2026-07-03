# Scénarios de démonstration (soutenance)

Exécuter **avant** la présentation ; joindre captures d’écran au rapport / Excel.

Dernière mise à jour : **23 juin 2026** — aligné sur [`architecture.md`](./architecture.md) et [`status-2026-06-23.md`](./status-2026-06-23.md).

## Variables labo

| Variable | Valeur |
|----------|--------|
| `IP_PUBLIQUE` | `78.202.114.212` |
| `PF_WAN` | `192.168.102.103` |
| `PF_LAN` | `192.168.10.1` |
| `BASTION` | `192.168.10.11` |
| `CLIENT` | `192.168.10.10` |
| `INFRASERVICE` | `192.168.10.15` |
| `NETBOX` | `http://192.168.10.15:8000` |
| `VAULT` | `http://192.168.10.15:8200` |
| `DOMAINE` | `mar2.local` |

---

## A — VPN site-à-site et client-à-site ✅

1. Établir le tunnel **IPsec** (client-à-site ou site-à-site selon pfSense).
2. Depuis le poste connecté :

```bash
ping -c 3 192.168.102.11
ping -c 3 192.168.10.15
traceroute 192.168.10.15
```

Attendu : reachabilité des réseaux distants, perte 0 %.

3. Vérifier l’état du tunnel dans pfSense : **VPN > IPsec > Status**.

> **Legacy :** la phase initiale utilisait OpenVPN UDP 1194 (`configs/openvpn/`). Les preuves IPsec remplacent ce scénario.

---

## B — Site interne (accès restreint) ✅

1. **Avec VPN** :

```bash
curl -I http://192.168.10.11
```

Attendu : `HTTP/1.1 200 OK`.

2. **Sans VPN** (réseau public) :

```bash
curl -I --connect-timeout 5 http://78.202.114.212
curl -I --connect-timeout 5 http://192.168.10.11
```

Attendu : timeout ou refus — pas d’exposition HTTP directe.

---

## C — Site distant depuis l’extérieur (bastion) ✅

1. Port ouvert :

```bash
nc -vz -G 5 78.202.114.212 2222
```

2. SSH :

```bash
ssh -p 2222 bastion@78.202.114.212
```

3. Depuis le bastion, reachabilité interne :

```bash
ping -c 3 192.168.10.10
ping -c 3 192.168.10.15
```

4. Variante Guacamole : connexion via interface web (LAN/VPN).

---

## D — Pare-feu : autorisé vs bloqué ✅

| Test | Commande | Attendu |
|------|----------|---------|
| IPsec ouvert | État tunnel pfSense + ping LAN distant | tunnel UP |
| SSH 22 public fermé | `nc -vz -G 5 78.202.114.212 22` | timeout |
| HTTP WAN fermé | `nc -vz -G 5 78.202.114.212 80` | timeout |
| SSH bastion via 2222 | `nc -vz -G 5 78.202.114.212 2222` | succeeded |

Capture pfSense : `Firewall > Rules > WAN` + `VPN > IPsec`.

---

## E — DNS (`mar2.local`) ✅

Depuis le bastion :

```bash
nslookup client1.site2.local 192.168.10.1
nslookup netbox.mar2.local
```

Attendu : résolution correcte (`192.168.10.10` pour client1).

---

## F — NetBox 🟢

1. Ouvrir NetBox : `http://192.168.10.15:8000`
2. Montrer sites, préfixes, VLAN et équipements documentés.
3. Lancer synchronisation :

```bash
export NETBOX_URL=http://192.168.10.15:8000
export NETBOX_TOKEN=<depuis Vault ou coffre>
python3 configs/netbox/scripts/sync_from_inventory.py --dry-run
```

Puis playbook :

```bash
cd iac/ansible
ansible-playbook playbooks/netbox-sync.yml --check
```

**Reste à faire :** compléter l’inventaire NetBox (VMs, équipements, tous les préfixes).

---

## G — Observabilité (Wazuh) 🟡

1. Générer un événement (connexion SSH bastion, refus firewall, ou commande test).
2. Ouvrir le dashboard Wazuh (`wazuh.mar2.local` ou IP manager).
3. Vérifier l’agent sur `infraservice` et le bastion.
4. Montrer une alerte ou un événement de sécurité dans l’interface.

**Reste à faire :** finaliser dashboards et alertes ; joindre captures à la soutenance.

> Legacy ELK/Kibana : voir `configs/elastic/kibana-guide.md` (phase initiale).

---

## H — Kill switch 🟡

Suivre [`drp-runbook.md`](./drp-runbook.md) :

1. Couper le tunnel IPsec (désactiver phase 1/2 ou règle WAN associée) **ou** utiliser l’API Kill Switch (quand disponible).
2. Vérifier : client VPN ne ping plus `192.168.102.11` ni `192.168.10.15`.
3. Rollback < 10 min, re-tester le tunnel.
4. Chronomètre + captures pfSense.

```bash
./scripts/kill-switch-s2.sh status
```

---

## I — Vault et Ansible (bonus IaC) 🟢

1. Vérifier Vault : `vault status` sur `infraservice` (via SSH).
2. Montrer la lecture d’un secret via Ansible AppRole (sans afficher le secret à l’oral).
3. Mentionner les snapshots Raft automatisés.

---

## J — Terraform (bonus IaC) 🟡

```bash
cd iac/terraform
terraform init && terraform validate && terraform plan
```

Montrer la connexion API Proxmox. Expliquer le blocage actuel : template `ubuntu-template` manquant.

**Reste à faire :** créer le template Cloud-Init, exécuter `terraform apply`, enchaîner Ansible.
