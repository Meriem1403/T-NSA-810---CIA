# pfSense — Site 2 (VM 100) — règles documentées

Exports GUI complets **non versionnés** (mots de passe). Ce fichier résume l’état validé en labo pour la soutenance.

## Interfaces

| Interface | Rôle | Adresse |
|-----------|------|---------|
| WAN | Vers box / Internet | `192.168.102.103` |
| LAN | Réseau interne S2 | `192.168.10.1/24` |

## NAT / Port Forward (WAN)

| Description | Proto | WAN port | Redirect | Preuve |
|-------------|-------|----------|----------|--------|
| SSH to Bastion (pfSense) | TCP | 22 | `192.168.10.11:22` | SSH via VPN `192.168.102.103` |
| *(Box externe)* | TCP | 2222 → WAN:22 | chaîne vers bastion | `nc` / `ssh -p 2222` public OK |

## Firewall WAN (résumé)

| # | Action | Proto | Port | Destination | Notes |
|---|--------|-------|------|-------------|-------|
| 1 | Pass | UDP | 1194 | WAN | OpenVPN |
| 2 | Pass | TCP | 22 | WAN → NAT bastion | Associée au port forward |
| — | Block implicite | * | 80, 443, autres | WAN | Pas de service web public |

## OpenVPN

- Serveur : UDP **1194** sur WAN.
- Tunnel : `10.8.0.0/24`.
- Routes poussées : LAN S2 + routes vers S1 (selon config serveur).

## DNS Resolver

- **Host override** : `client1.site2.local` → `192.168.10.10`
- **Domain override** : `site2.local` → `192.168.10.1`

## Kill switch (référence)

| Action | Emplacement |
|--------|-------------|
| Couper VPN entrant | `Firewall > Rules > WAN` — désactiver règle UDP 1194 |
| Rollback | Réactiver règle + `Apply` — tester `ping` via tunnel |

Captures recommandées pour le rapport : onglets **WAN rules**, **NAT**, **OpenVPN status**.
