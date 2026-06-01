# Kibana — analyse et visualisation (soutenance)

## Accès

- URL : `http://192.168.199.20:5601`
- Utilisateur : `elastic` / mot de passe défini dans `vault.yml`

## Discover — logs bastion

1. **Stack Management** → **Index Patterns** → Create `filebeat-*` (timestamp `@timestamp`).
2. **Discover** → index `filebeat-*`.
3. Filtres utiles :
   - `site: "site2"`
   - `role: "bastion"` ou `bastion-nginx`
   - `message: *Failed*` (échecs SSH)

## Dashboard de démo (manuel)

Créer un dashboard « CIA — Bastion » avec :

| Visualisation | Type | Champ |
|---------------|------|-------|
| Connexions SSH / heure | Lens / histogram | `@timestamp` |
| Top messages auth | Data table | `message.keyword` |
| Répartition site | Pie | `site.keyword` |

Exporter : **Stack Management** → **Saved Objects** → Export (joindre au rapport, sans credentials).

## Événement de test

```bash
ssh -p 2222 bastion@78.202.114.212 "logger 'CIA-KIBANA-TEST'"
```

Rechercher `CIA-KIBANA-TEST` dans Discover (< 2 min).
