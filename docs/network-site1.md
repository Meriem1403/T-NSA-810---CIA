# Spécifications réseau — Site 1 (On-prem)

Document pour le trophée `network_spec1`.

## Identité du site

| Attribut | Valeur |
|----------|--------|
| Nom | Site 1 — On-prem |
| Hyperviseur | Proxmox 02 |
| Rôle | Site principal, identité, routage vers S2 |
| Domaine | `mar2.local` |

## Plan d'adressage

| Segment | CIDR | Passerelle | Usage |
|---------|------|------------|-------|
| LAN S1 | `192.168.199.0/24` | `192.168.199.1` | Réseau interne site 1 |
| VPN IPsec | (tunnel) | pfSense | Interconnexion S1 ↔ S2 |

### Hôtes principaux

| Hôte | IP | Rôle |
|------|-----|------|
| fw-s1 (pfSense) | `192.168.199.1` | Pare-feu, routeur, terminateur VPN |
| Proxmox S1 | `192.168.199.131` | Hyperviseur (exemple labo) |
| Contrôleur AD | DHCP/DNS AD | DNS `mar2.local` |
| svc-s1 (cible) | `192.168.199.20` | Modèle hybride services (optionnel) |

## Interfaces pfSense S1

| Interface | Réseau | Description |
|-----------|--------|-------------|
| LAN | `192.168.199.0/24` | Réseau interne |
| WAN / IPsec | Tunnel vers S2 | VPN site-à-site |

Voir [`../configs/pfsense/site1-lan-rules.md`](../configs/pfsense/site1-lan-rules.md).

## Routage

| Destination | Next-hop | Mécanisme |
|-------------|----------|-----------|
| `192.168.10.0/24` (S2) | Tunnel IPsec | Phase 2 IPsec pfSense |
| Internet | WAN S1 | NAT sortant pfSense |
| `mar2.local` | DNS AD | Résolution interne |

## DNS Site 1

| Zone | Serveur | Type |
|------|---------|------|
| `mar2.local` | Contrôleur AD | Autoritative |
| Forwarders externes | pfSense ou AD | Résolution Internet |

Enregistrements prévus :

| Nom | Type | Cible |
|-----|------|-------|
| `netbox.mar2.local` | A | `192.168.10.15` (service hébergé S2 en labo) |
| `vault.mar2.local` | A | `192.168.10.15` |
| `wazuh.mar2.local` | A | `192.168.10.15` |

## Règles pare-feu (résumé)

| Direction | Action | Détail |
|-----------|--------|--------|
| LAN → IPsec (S2) | Autoriser | Administration cross-site |
| IPsec → LAN | Autoriser | Retour, services AD |
| LAN → Internet | Autoriser (stateful) | Sortie utilisateurs |
| Internet → LAN | Refuser | Pas d'exposition directe |

## Tests de validation

```bash
# Depuis un hôte S1 (ou via VPN)
ping 192.168.10.1      # pfSense S2 via tunnel
ping 192.168.10.15     # InfraService
nslookup mar2.local    # DNS AD
```

## Preuves soutenance

- 📸 Interface pfSense S1 — onglet Interfaces
- 📸 IPsec Phase 1/2 configurée
- 📸 Règles firewall LAN
- 📸 `ipconfig /all` ou `resolvectl status` sur poste AD

## Références

- [`architecture.md`](./architecture.md)
- [`network-site2.md`](./network-site2.md)
- [`configs/dns/forwarders.md`](../configs/dns/forwarders.md)
