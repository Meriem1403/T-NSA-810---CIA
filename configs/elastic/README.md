# Elasticsearch / stack observabilité

Conseillé de versionner :

- `filebeat.yml` **template** (hosts Elastic en variable).
- `metricbeat.d/` ou équivalent.
- Export **NDJSON** d’un dashboard Kibana de démo (sans credentials).
- Pipelines ingest si utilisés.

Les mots de passe cluster : coffre + `ELASTIC_PASSWORD` en CI locale.
