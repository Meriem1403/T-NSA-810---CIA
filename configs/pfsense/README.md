# pfSense — configuration versionnée

- Exports GUI **sanitisés** : remplacer mots de passe par `REDACTED`.
- Règles documentées en **tableaux Markdown** :

| Site | Fichier | Trophée |
|------|---------|---------|
| Site 1 (on-prem) | [`site1-lan-rules.md`](./site1-lan-rules.md) | `network_firewall`, `network_spec1` |
| Site 2 (remote) | [`site2-wan-rules.md`](./site2-wan-rules.md) | `network_firewall`, `network_vpn`, `network_spec2` |

Documenter WAN / LAN / IPsec et kill switch (onglet / section pfSense).

Voir [`../../docs/trophees-validation.md`](../../docs/trophees-validation.md).
