# pfSense — Site 2 (VM 100) — règles documentées

Exports GUI complets **non versionnés** (mots de passe). Résumé validé en labo pour trophées `network_firewall` et `network_vpn`.

## Interfaces

| Interface | Rôle | Adresse |
|-----------|------|---------|
| WAN | Vers box / Internet | `192.168.102.103` |
| LAN | Réseau interne S2 | `192.168.10.1/24` |

## VPN IPsec (production labo)

| Paramètre | Valeur |
|-----------|--------|
| Type | Site-à-site + client-à-site |
| Protocole | IKEv2 / IPsec |
| Ports WAN | UDP 500, UDP 4500, ESP |
| Réseau local S2 | `192.168.10.0/24` |
| Réseau distant S1 | `192.168.199.0/24` |
| Secrets | PSK / certificats — **hors Git** (Vault ou coffre) |

Vérification : **VPN > IPsec > Status** → tunnel UP.

> **Legacy phase 1 :** OpenVPN UDP 1194 (`configs/openvpn/server-notes.md`) — conservé pour historique.

## NAT / Port Forward (WAN)

| Description | Proto | WAN port | Redirect | Preuve |
|-------------|-------|----------|----------|--------|
| SSH bastion (via box) | TCP | 2222 → WAN | chaîne vers `192.168.10.11:22` | `ssh -p 2222` public OK |
| SSH pfSense (VPN) | TCP | 22 | `192.168.10.11:22` | SSH via VPN WAN IP |

## Firewall WAN (résumé)

| # | Action | Proto | Port / type | Notes |
|---|--------|-------|-------------|-------|
| 1 | Pass | UDP | 500, 4500 | IKE/IPsec |
| 2 | Pass | ESP | — | IPsec data |
| 3 | Pass | TCP | 22 (NAT bastion) | Accès admin contrôlé |
| — | Block implicite | * | 80, 443, 22 direct | Pas de service web/SSH public |

## Firewall LAN (résumé)

| # | Action | Source | Destination |
|---|--------|--------|-------------|
| 1 | Pass | LAN | IPsec (S1) |
| 2 | Pass | IPsec | LAN |
| 3 | Pass | LAN | Internet (NAT) |

## DNS Resolver

| Type | Nom | Cible |
|------|-----|-------|
| Host override | `client1.site2.local` | `192.168.10.10` |
| Domain override | `site2.local` | `192.168.10.1` |

Détails : [`../dns/forwarders.md`](../dns/forwarders.md).

## Kill switch

| Action | Emplacement |
|--------|-------------|
| Couper VPN entrant | `VPN > IPsec` — disable Phase 1 **ou** `Firewall > WAN` — bloquer UDP 500/4500 |
| Couper bastion public | Retirer NAT box `2222` |
| Rollback | Réactiver + Apply — tester `ping` via tunnel |

Script : [`../../scripts/kill-switch-s2.sh`](../../scripts/kill-switch-s2.sh).

## Captures recommandées

- WAN rules + IPsec rules
- NAT port forward 2222
- IPsec Status (tunnel UP)
- OpenVPN status (si legacy encore actif)
