# Génération automatique — présentation PowerPoint

Génère `docs/presentations/CIA-Soutenance-T-NSA-810.pptx` à partir de la documentation du projet.

## Prérequis

- Python 3.10+
- Dépendances : `python-pptx`, `Pillow`

## Génération (une commande)

```bash
./scripts/presentation/build.sh
```

Ou manuellement :

```bash
python3 -m venv .venv-presentation
.venv-presentation/bin/pip install -r scripts/presentation/requirements.txt
.venv-presentation/bin/python scripts/presentation/generate_presentation.py
```

## Contenu généré (~18 slides, format 16:9)

| # | Slide | Contenu |
|---|-------|---------|
| 1 | Couverture | Titre, équipe, date — design navy/teal |
| 2 | Agenda | 8 sections numérotées |
| 3 | Problématique | Objectif, contraintes, résultat (cartes) |
| 4 | Bilan 90 % | Stats + tableau composants |
| 5 | Timeline F0–F11 | Parcours du projet |
| 6 | Équipe | Meriem vs Kévin — détail du travail |
| 7 | Architecture | Diagramme PNG encadré + cartes sites |
| 8 | Site 2 détaillé | VMs, IPs, ce qu'on a configuré, preuves |
| 9 | VPN IPsec | Avant/après OpenVPN, commandes démo |
| 10 | Pare-feu & bastion | Tableau tests + explications |
| 11 | InfraService | 6 cartes services |
| 12 | NetBox & Vault | Automatisation détaillée |
| 13 | Wazuh | Logs centralisés, évolution ELK |
| 14 | Ansible & Terraform | Playbooks, rôles, état TF |
| 15 | Kill switch & DRP | Procédure + checklist |
| 16 | Dépôt Git | Arborescence + 29 trophées |
| 17 | Démo live | 8 commandes en cartes |
| 18 | Conclusion | Synthèse + questions |

## Personnalisation

Éditer `scripts/presentation/generate_presentation.py` puis relancer `build.sh`.

Le diagramme est importé depuis `docs/architecture-diagram.png`.

## Fichiers

| Fichier | Rôle |
|---------|------|
| `generate_presentation.py` | Script Python principal |
| `requirements.txt` | Dépendances pip |
| `build.sh` | Lanceur bash |
| `docs/presentations/*.pptx` | Sortie générée |

L'environnement virtuel `.venv-presentation/` est gitignored.
