# Scénarios de démonstration (soutenance)

À exécuter avant la présentation ; annexer captures pour le rapport.

## A — VPN site-à-site

1. Connexion cliente OpenVPN réussie avec logs courts.
2. `ping` / `traceroute` d’un LAN vers l’autre via préfixe distant.

## B — Site interne (on-prem)

1. OK depuis LAN ou VPN déjà connecté.
2. Refus / injoignable depuis hors réseau autorisé (si démo possible).

## C — Site distant depuis l’extérieur

1. `ssh -J bastion@IP_PUBLIQUE user@interne`
2. Montrer l’impossibilité d’atteindre la VM interne directement sans bastion sur IP WAN.

## D — Pare-feu séparation du trafic

1. Tester un flux **explicitement bloqué** (ex. DMZ→Admin) ; montrer la règle pfSense correspondante.

## E — DNS forwarding

1. Résoudre depuis S1 un FQDN réservé au site S2 comme dans la documentation.

## F — NetBox

1. Présenter l’entrée équipe/réseaux ; évolution automatique après script ou playbook démo.

## G — Observabilité

1. Requête / dashboard montrant un événement récent (VPN, denial firewall, bastion SSH).

## H — Kill switch

1. Appliquer la procédure `drp-runbook.md` puis revenir sous 10 minutes.
