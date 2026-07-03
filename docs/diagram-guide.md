# Guide des diagrammes — CIA

Documents pour les trophées `diagram_delivery` et `diagram_quality`.

## Fichiers livrés

| Fichier | Format | Usage |
|---------|--------|-------|
| [`architecture-diagram.png`](./architecture-diagram.png) | PNG | Soutenance, rapport, slides |
| [`architecture-diagram.mmd`](./architecture-diagram.mmd) | Mermaid | Source versionnée, régénération |
| [`architecture.md`](./architecture.md) | Markdown | Schéma Mermaid inline + tables |

## Régénérer le PNG

```bash
npx @mermaid-js/mermaid-cli -i docs/architecture-diagram.mmd -o docs/architecture-diagram.png
```

## Critères de qualité (`diagram_quality`)

Le diagramme doit permettre à un correcteur de comprendre **sans oral** :

| Critère | Présent ? | Détail |
|---------|-----------|--------|
| Deux sites identifiables | ✅ | S1 On-prem + S2 Remote |
| Internet / IP publique | ✅ | `78.202.114.212` |
| Pare-feu nommés | ✅ | pfSense S1 + S2 (CARP) |
| VPN explicite | ✅ | Tunnel IPsec entre sites |
| Services nommés | ✅ | NetBox, Vault, Wazuh, bastion, AD |
| Adresses IP clés | ✅ | `.10.1`, `.10.11`, `.10.15`, `.199.1` |
| Flux directionnels | ✅ | Flèches Internet → box → pfSense → LAN |
| Légende implicite | ✅ | Subgraphs par site |

## Éléments obligatoires du schéma

```text
[Internet]
    ↓
[Box NAT 2222]
    ↓
[pfSense S2 — WAN/LAN]
    ├── [bastion + nginx]
    ├── [client Windows]
    ├── [infraservice — NetBox/Vault/Wazuh]
    └── [Guacamole]
    ↕ IPsec
[pfSense S1]
    └── [AD mar2.local — LAN 192.168.199.0/24]
```

## Améliorations recommandées (slides)

Pour la soutenance, enrichir une slide avec :

- Code couleur : rouge = Internet, bleu = VPN, vert = LAN interne
- Numéros de VLAN si utilisés
- Ports exposés (2222, 8000, 8200) en annotation

## Outils acceptés

- **Mermaid** (versionné dans le dépôt) — recommandé
- Draw.io / Excalidraw — export PNG à ajouter dans `docs/` si complément
- pfSense diagram export — capture pour preuve firewall

## Preuves à joindre

| Capture | Trophée |
|---------|---------|
| `architecture-diagram.png` dans le dépôt | `diagram_delivery` |
| Slide agrandie lisible en projection | `diagram_quality` |
| Photo schéma au tableau lors de la soutenance | Bonus clarté |
