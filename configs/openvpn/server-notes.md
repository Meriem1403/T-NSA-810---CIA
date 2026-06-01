# OpenVPN — Site 2 (notes sans secrets)

## Paramètres serveur (pfSense)

| Paramètre | Valeur labo |
|-----------|-------------|
| Protocole | UDP |
| Port local | 1194 |
| Réseau tunnel | `10.8.0.0/24` |
| Interface | WAN |

## Client

- Fichier `.ovpn` généré depuis pfSense : **ne pas commiter** (`.gitignore`).
- Tester : `openvpn --config client-s2.ovpn` ou client GUI.

## Routes attendues côté client (Mac)

Après connexion, route vers LAN distant :

```text
192.168.102.0/24  → utun*
```

## Dépannage rapide

| Symptôme | Piste |
|----------|-------|
| UDP 1194 fermé | Règle WAN + NAT box |
| Tunnel up, pas de ping LAN | Routes poussées serveur / firewall LAN |
| Instabilité après veille | Reconnexion client ; vérifier keepalive serveur |
