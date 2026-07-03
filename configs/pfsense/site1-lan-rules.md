# pfSense — Site 1 (fw-s1) — règles documentées

Exports GUI complets **non versionnés** (mots de passe). Résumé pour trophée `network_firewall` (site 1).

## Interfaces

| Interface | Rôle | Adresse |
|-----------|------|---------|
| LAN | Réseau interne S1 | `192.168.199.1/24` |
| WAN / IPsec | Internet + tunnel S2 | Selon uplink S1 |

## Routage IPsec

| Phase | Paramètre | Valeur |
|-------|-----------|--------|
| Phase 1 | Protocole | IKEv2 |
| Phase 1 | Authentification | PSK ou certificats (hors Git) |
| Phase 2 | Réseaux locaux | `192.168.199.0/24` |
| Phase 2 | Réseaux distants | `192.168.10.0/24` |

## Firewall LAN (résumé)

| # | Action | Source | Destination | Notes |
|---|--------|--------|-------------|-------|
| 1 | Pass | LAN net | IPsec net (S2) | Administration cross-site |
| 2 | Pass | IPsec net | LAN net | Retour trafic |
| 3 | Pass | LAN net | LAN net | Trafic interne |
| 4 | Pass | LAN net | any (Internet) | Sortie NAT stateful |
| — | Block | any | LAN net (depuis WAN) | Pas d'entrée directe Internet |

## Firewall IPsec (résumé)

| # | Action | Détail |
|---|--------|--------|
| 1 | Pass | Trafic chiffré S1 ↔ S2 autorisé |
| 2 | Pass | ICMP (diagnostic ping inter-sites) |

## DNS / AD

- Zone autoritative : `mar2.local`
- Forwarders vers services S2 documentés dans [`../dns/forwarders.md`](../dns/forwarders.md)

## Tests de validation

```bash
# Depuis poste S1
ping 192.168.10.1       # pfSense S2 via tunnel
ping 192.168.10.15      # InfraService
nslookup mar2.local
```

## Kill switch (site 1)

| Action | Lieu |
|--------|------|
| Couper tunnel S2 | `VPN > IPsec` — disable Phase 1 |
| Isoler LAN S1 | Suspendre règle LAN → IPsec |

Rollback : réactiver Phase 1/2, vérifier `ping` inter-sites.

## Captures recommandées

- Interfaces LAN/WAN
- IPsec Phase 1 & 2
- Firewall rules LAN
- Statut tunnel UP
