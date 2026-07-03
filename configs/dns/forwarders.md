# DNS — domaine `mar2.local` et forwarders

Document pour le trophée `network_dns`.

## Architecture DNS

| Zone / domaine | Serveur autoritaire | Site |
|---------------|---------------------|------|
| `mar2.local` | Active Directory (S1) | Site 1 |
| `site2.local` | pfSense Resolver (S2) | Site 2 |
| Résolution externe | Forwarders pfSense / AD | Les deux sites |

## Enregistrements `mar2.local` (AD)

| Nom | Type | Cible | Service |
|-----|------|-------|---------|
| `dc01.mar2.local` | A | IP contrôleur AD | Contrôleur de domaine |
| `netbox.mar2.local` | A | `192.168.10.15` | NetBox IPAM |
| `vault.mar2.local` | A | `192.168.10.15` | HashiCorp Vault |
| `wazuh.mar2.local` | A | `192.168.10.15` | Wazuh manager |
| `api.mar2.local` | A | `192.168.10.15` | API Kill Switch (futur) |

## Overrides pfSense S2

| Type | Nom | Valeur |
|------|-----|--------|
| Host override | `client1.site2.local` | `192.168.10.10` |
| Domain override | `site2.local` | Forwarder `192.168.10.1` |

Configuration GUI : **Services > DNS Resolver > Host Overrides**.

## Forwarders inter-sites

| Site | Forward vers | Objectif |
|------|--------------|----------|
| S2 → S1 | IP contrôleur AD | Résoudre `*.mar2.local` |
| S1 → S2 | `192.168.10.1` (pfSense S2) | Résoudre `*.site2.local` |

## Template pfSense — Domain Override

```text
# Services > DNS Resolver > Domain Overrides
Domain: mar2.local
IP: <IP_DNS_AD_S1>
Description: Forward to Site 1 AD
```

## Template Windows DNS — Conditional Forwarder

```powershell
# Sur contrôleur AD (exemple — adapter IP)
Add-DnsServerConditionalForwarderZone -Name "site2.local" -MasterServers 192.168.10.1
```

## Tests de validation

```bash
# Depuis bastion S2
nslookup client1.site2.local 192.168.10.1
# Attendu : 192.168.10.10

nslookup netbox.mar2.local
# Attendu : 192.168.10.15

# Depuis poste S1
nslookup bastion.site2.local
# Attendu : 192.168.10.11 (si enregistré dans AD ou forwarder)
```

## Preuves soutenance

- 📸 pfSense Host Overrides
- 📸 AD DNS Manager — zone `mar2.local`
- 📸 Sortie `nslookup` réussie

## Références

- [`../../docs/network-site1.md`](../../docs/network-site1.md)
- [`../../docs/network-site2.md`](../../docs/network-site2.md)
- [`../../docs/demo-scenarios.md`](../../docs/demo-scenarios.md) § E
