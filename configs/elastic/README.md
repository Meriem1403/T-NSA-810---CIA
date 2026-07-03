# Elasticsearch / stack observabilité (legacy)

> **Statut :** phase initiale du labo. La supervision courante utilise **Wazuh** sur `infraservice` (`192.168.10.15`). Voir [`../../docs/architecture.md`](../../docs/architecture.md#observabilité-wazuh).

Fichiers conservés à titre d’archive :

- `filebeat.yml.example` — template Filebeat (hosts Elastic en variable).
- `kibana-guide.md` — guide Discover/dashboards Kibana (phase initiale).

Les playbooks Ansible `deploy-site1.yml` et `deploy-observability.yml` déploient encore cette stack si besoin de démo ELK.

Pour la soutenance : privilégier **captures Wazuh** (dashboards, alertes, agents).

Les mots de passe cluster : Vault (`infra/elastic`) ou coffre — jamais dans Git.
