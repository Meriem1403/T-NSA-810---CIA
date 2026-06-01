# Scénarios de démonstration (soutenance)

Exécuter **avant** la présentation ; joindre captures d’écran au rapport / Excel.

Variables labo S2 (à adapter si IP changent) :

| Variable | Valeur |
|----------|--------|
| `IP_PUBLIQUE` | `78.202.114.212` |
| `PF_WAN` | `192.168.102.103` |
| `PF_LAN` | `192.168.10.1` |
| `BASTION` | `192.168.10.11` |
| `CLIENT` | `192.168.10.10` |

---

## A — VPN site-à-site ✅

1. Connexion client OpenVPN vers `IP_PUBLIQUE:1194`.
2. Depuis le Mac connecté :

```bash
ping -c 3 192.168.102.11
traceroute 192.168.102.11
netstat -rn | egrep "192.168.102|utun|tun"
```

Attendu : passage par `10.8.0.1`, perte 0 %.

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
```

4. Variante VPN :

```bash
ssh bastion@192.168.102.103
```

---

## D — Pare-feu : autorisé vs bloqué ✅

| Test | Commande | Attendu |
|------|----------|---------|
| VPN ouvert | `nc -vzu 78.202.114.212 1194` | succeeded |
| SSH 22 public fermé | `nc -vz -G 5 78.202.114.212 22` | timeout |
| HTTP WAN fermé | `nc -vz -G 5 78.202.114.212 80` | timeout |
| SSH bastion via 2222 | `nc -vz -G 5 78.202.114.212 2222` | succeeded |

Capture pfSense : `Firewall > Rules > WAN` + `NAT > Port Forward`.

---

## E — DNS forwarding ✅

Depuis le bastion :

```bash
nslookup client1.site2.local 192.168.10.1
```

Attendu : `192.168.10.10`.

---

## F — NetBox ⏳

1. Ouvrir NetBox (site S1) — URL à documenter.
2. Montrer préfixes `site1` / `site2`.
3. Lancer synchronisation :

```bash
export NETBOX_URL=https://netbox.example.local
export NETBOX_TOKEN=<depuis coffre>
python3 configs/netbox/scripts/sync_from_inventory.py --dry-run
```

Puis playbook :

```bash
cd iac/ansible
ansible-playbook playbooks/netbox-sync.yml --check
```

---

## G — Observabilité ⏳

1. Générer un événement (connexion SSH bastion ou refus firewall).
2. Kibana : dashboard « SSH / firewall » — voir `configs/elastic/`.

---

## H — Kill switch ⏳

Suivre [`drp-runbook.md`](./drp-runbook.md) section S2 :

1. Désactiver règle WAN UDP 1194 **ou** arrêter OpenVPN.
2. Vérifier : client VPN ne ping plus le LAN distant.
3. Rollback < 10 min, re-tester ping VPN.
