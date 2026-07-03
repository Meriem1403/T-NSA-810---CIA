# Guide observabilité — logs, analyse et visualisations

Documents pour les trophées `log_centralisation`, `log_observability`, `log_analysis`, `log_visuals`.

## Architecture observabilité

| Composant | Hôte | Rôle |
|-----------|------|------|
| Wazuh manager | `infraservice` (`192.168.10.15`) | Collecte, corrélation, alertes |
| Wazuh agents | bastion, infraservice, autres VMs | Envoi logs système, audit, FIM |
| Interface web | `wazuh.mar2.local` ou IP manager | Dashboards, Discover, alertes |

> **Legacy :** stack Elastic + Filebeat (`configs/elastic/`, playbook `deploy-observability.yml`) — phase initiale, conservée à titre d'archive.

## Centralisation (`log_centralisation`)

### Flux de logs

```text
[VM bastion]  ──agent──┐
[VM client]   ──agent──┼──► [Wazuh manager :1514] ──► [Index stockage]
[infraservice]──agent──┘
```

### Vérification agent connecté

1. Wazuh UI → **Agents** → statut `Active`
2. Depuis l'agent : `systemctl status wazuh-agent`

### Événement de test

```bash
ssh -p 2222 bastion@78.202.114.212 "logger 'CIA-WAZUH-TEST-$(date +%s)'"
```

Attendu : événement visible dans Wazuh < 2 minutes.

### Preuves

- 📸 Liste agents avec statut Active (≥ 2 agents)
- 📸 Événement `CIA-WAZUH-TEST` dans les logs

---

## Observabilité (`log_observability`)

### Métriques et états surveillés

| Source | Données |
|--------|---------|
| Syslog | auth.log, daemon.log |
| Auditd | Connexions SSH, sudo |
| pfSense | Logs firewall (si forward configuré) |
| Wazuh FIM | Intégrité fichiers critiques |

### Dashboards recommandés

| Dashboard | Contenu |
|-----------|---------|
| Agents overview | Nombre agents, OS, dernière activité |
| Security events | Alertes niveau ≥ 7 |
| SSH authentication | Succès / échecs connexion |

### Commandes de vérification

```bash
# Sur infraservice (manager)
curl -k -u wazuh:wazuh https://localhost:55000/agents?pretty=true

# Sur agent bastion
sudo tail -f /var/ossec/logs/ossec.log
```

---

## Analyse (`log_analysis`)

### Cas d'usage démontrables en soutenance

| Scénario | Comment déclencher | Où voir |
|----------|-------------------|---------|
| Connexion SSH réussie | `ssh bastion@...` | Wazuh → Security Events |
| Échec SSH (mauvais mdp) | 3 tentatives invalides | Alerte brute-force |
| Commande sudo | `sudo logger test` | auth.log analysé |
| Scan port (optionnel) | `nmap` depuis VM test | Alerte scan détecté |

### Filtres Wazuh utiles

```text
rule.level:>=7
data.srcip:192.168.10.*
full_log:*CIA-WAZUH-TEST*
```

### Corrélation avec sécurité

- Lier une alerte Wazuh au **kill switch** (objectif F10) : blocage IP source automatique.
- Documenter dans [`drp-runbook.md`](./drp-runbook.md).

---

## Visualisations (`log_visuals`)

### Dashboards à préparer

| Visualisation | Type | Champ / règle |
|---------------|------|---------------|
| Événements par heure | Histogram | `@timestamp` |
| Top règles déclenchées | Table | `rule.description` |
| Agents par statut | Pie chart | `agent.name` |
| Échecs SSH | Bar chart | `rule.id` auth failures |

### Création dans Wazuh

1. **Modules** → **Security Events**
2. Filtrer période soutenance
3. Créer visualisation personnalisée
4. Exporter capture PNG pour rapport

### Alternative legacy (Elastic/Kibana)

Si démo ELK nécessaire :

```bash
# Kibana : http://192.168.10.15:5601 (si stack legacy active)
# Index pattern : filebeat-*
# Voir configs/elastic/kibana-guide.md
```

---

## Checklist trophées logs

| Trophée | Action | Fait |
|---------|--------|------|
| `log_centralisation` | 2+ agents actifs, log test reçu | ☐ |
| `log_observability` | Dashboard agents + métriques | ☐ |
| `log_analysis` | Alerte ou filtre sur échec SSH | ☐ |
| `log_visuals` | Capture dashboard Wazuh | ☐ |

## Références

- [`configs/wazuh/README.md`](../configs/wazuh/README.md)
- [`demo-scenarios.md`](./demo-scenarios.md) § G
- [`deploy-lab.md`](./deploy-lab.md) § 5
