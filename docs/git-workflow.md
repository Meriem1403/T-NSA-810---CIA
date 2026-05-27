# Flux Git — pour la grille « pratiques de dépôt »

## Branches

- `main` : état présentable + doc alignée infra réelle.
- `feature/` : périmètre limité par sujet VPN, bastion, NetBox…
- `fix/` : correctifs playbook ou docs.

## Commits

Forme conseillée :

- `feat(vpn): snippet server.conf sans secrets`
- `docs(architecture): mise à jour schéma S2`
- `fix(ansible): handler restart openvpn`

## Interdictions

Aucune clé, cert ni `.ovpn` complet dans l’historique : voir `.gitignore`.

## Pull Requests

Description + liste de tests manuels effectués avant merge vers `main`.
