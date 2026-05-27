# OpenVPN — extraits sans secrets

Stocker uniquement :

- `server-snippet.conf` et `client-snippet.conf` **avec chemins relatifs génériques**.
- Scripts `ccd/` pour routes LAN **sans clefs**.
- Une copie anonymisée de `iptables`/`pf` si hors pfSense GUI.

Exporter les **CSR / certificats** uniquement hors dépôt (coffre partagé encadrant).
