# Spécifications réseau — Site 2 (Remote)

Document pour le trophée `network_spec2`.

## Identité du site

| Attribut | Valeur |
|----------|--------|
| Nom | Site 2 — Remote |
| Hyperviseur | Proxmox 01 (`Proxmox-01`) |
| Rôle | Site distant Internet, DMZ, bastion, services |
| IP publique | `78.202.114.212` |

## Plan d'adressage

| Segment | CIDR | Passerelle | Usage |
|---------|------|------------|-------|
| WAN uplink | `192.168.102.0/24` | Box FAI | Internet, management Proxmox |
| LAN S2 | `192.168.10.0/24` | `192.168.10.1` | Réseau interne |
| VPN IPsec | (tunnel) | pfSense | Vers S1 + clients distants |

### VMs et hôtes

| VM ID | Nom | IP | Rôle |
|-------|-----|-----|------|
| 100 | FW | WAN `192.168.102.103` / LAN `192.168.10.1` | pfSense CARP |
| 101 | Client | `192.168.10.10` | Poste Windows interne |
| 102 | bastion-s2 | `192.168.10.11` | SSH, nginx site interne |
| — | infraservice | `192.168.10.15` | NetBox, Vault, Wazuh, IaC |
| — | Proxmox | `192.168.102.11` | Hyperviseur `:8006` |

## Interfaces pfSense S2

| Interface | Adresse | Description |
|-----------|---------|-------------|
| WAN | `192.168.102.103/24` | Vers box Internet |
| LAN | `192.168.10.1/24` | Réseau interne S2 |

Voir [`../configs/pfsense/site2-wan-rules.md`](../configs/pfsense/site2-wan-rules.md).

## NAT / exposition contrôlée

| Service | WAN | Redirect | Justification |
|---------|-----|----------|---------------|
| SSH bastion (via box) | TCP 2222 | pfSense → `192.168.10.11:22` | Accès admin unique |
| IPsec | UDP 500, 4500, ESP | pfSense | VPN site-à-site + client |

**Non exposé :** HTTP/HTTPS direct, SSH port 22 public, Proxmox, NetBox, Vault.

## Segmentation

```text
Internet (78.202.114.212)
    │
    ▼
[Box NAT :2222]
    │
    ▼
[pfSense WAN 192.168.102.103]
    │
    ├── LAN 192.168.10.0/24
    │     ├── .10  Client
    │     ├── .11  Bastion + nginx
    │     └── .15  InfraService
    │
    └── IPsec tunnel → Site 1
```

## DNS Site 2 (pfSense Resolver)

| Type | Nom | Cible |
|------|-----|-------|
| Host override | `client1.site2.local` | `192.168.10.10` |
| Domain override | `site2.local` | `192.168.10.1` |

Détails : [`../configs/dns/forwarders.md`](../configs/dns/forwarders.md).

## Tests de validation

```bash
# Depuis Internet (sans VPN)
nc -vz -G 5 78.202.114.212 2222    # OK
nc -vz -G 5 78.202.114.212 22      # timeout
nc -vz -G 5 78.202.114.212 80      # timeout

# Via VPN
ping 192.168.10.15
curl -I http://192.168.10.11
ssh -p 2222 bastion@78.202.114.212
```

## Preuves soutenance

- 📸 pfSense — Interfaces WAN/LAN
- 📸 NAT Port Forward (2222)
- 📸 Firewall WAN rules
- 📸 Proxmox — liste VMs 100–102 + infraservice
- 📸 `curl -I http://192.168.10.11` depuis VPN (200 OK)

## Références

- [`architecture.md`](./architecture.md)
- [`demo-scenarios.md`](./demo-scenarios.md) § B, C, D
- [`network-site1.md`](./network-site1.md)
