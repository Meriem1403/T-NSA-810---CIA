# OpenVPN — extraits sans secrets (legacy)

> **Statut :** phase initiale du labo. Le VPN courant utilise **IPsec** (site-à-site + client-à-site) configuré sur pfSense. Voir [`../../docs/architecture.md`](../../docs/architecture.md).

Stocker uniquement :

- `server-snippet.conf` et `client-snippet.conf` **avec chemins relatifs génériques**.
- Scripts `ccd/` pour routes LAN **sans clefs**.
- Une copie anonymisée de `iptables`/`pf` si hors pfSense GUI.

Exporter les **CSR / certificats** uniquement hors dépôt (coffre partagé encadrant).

Notes labo phase 1 : [`server-notes.md`](./server-notes.md) (UDP 1194, réseau `10.8.0.0/24`).
