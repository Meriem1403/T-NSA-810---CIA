# Wazuh — supervision et SIEM

Configuration pour les trophées `log_centralisation`, `log_observability`, `log_analysis`, `log_visuals`.

## Déploiement labo

| Composant | Hôte | Accès |
|-----------|------|-------|
| Wazuh manager | `infraservice` (`192.168.10.15`) | `https://wazuh.mar2.local` ou IP |
| Wazuh indexer | même hôte (stack Docker ou package) | port 9200 (interne) |
| Wazuh dashboard | même hôte | port 443 / 5601 |

## Agents déployés

| Agent | Hôte | IP | Rôle |
|-------|------|-----|------|
| agent-bastion | bastion-s2 | `192.168.10.11` | SSH, nginx, syslog |
| agent-infra | infraservice | `192.168.10.15` | Services Docker, Vault |
| agent-client | (optionnel) | `192.168.10.10` | Poste Windows |

## Enrôlement agent (exemple Linux)

```bash
# Sur l'hôte agent — remplacer MANAGER_IP
curl -so wazuh-agent.deb https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.9.0-1_amd64.deb
WAZUH_MANAGER="192.168.10.15" dpkg -i wazuh-agent.deb
systemctl enable wazuh-agent && systemctl start wazuh-agent
```

## Événement de test

```bash
logger "CIA-WAZUH-TEST"
# ou
ssh -p 2222 bastion@78.202.114.212 "logger 'CIA-WAZUH-TEST'"
```

## Règles d'alerte recommandées (soutenance)

| Règle | Niveau | Déclencheur |
|-------|--------|-------------|
| SSH auth failure | ≥ 5 | 3+ échecs en 2 min |
| New agent connected | 3 | Agent enrôlé |
| Syscheck modified | ≥ 7 | Fichier critique modifié |

## Dashboards à créer

Voir [`../../docs/observability-guide.md`](../../docs/observability-guide.md) § Visualisations.

## Fichiers versionnables (futur)

- `ossec.conf` template (sans clés)
- Export dashboard JSON (sans credentials)
- Liste règles custom `local_rules.xml` (extraits sanitisés)

## Legacy

Stack Elastic + Filebeat : [`../elastic/`](../elastic/) — phase initiale avant migration Wazuh.

## Références

- [Wazuh Documentation](https://documentation.wazuh.com/)
- [`../../docs/demo-scenarios.md`](../../docs/demo-scenarios.md) § G
