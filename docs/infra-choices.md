# Choix techniques et versions — CIA

Document pour le trophée `infra_choices`.

## Principes de sélection

1. **Communauté active** — documentation, forums, mises à jour de sécurité.
2. **Interopérabilité** — intégration Ansible, API REST, standards (IPsec, LDAP).
3. **Reproductibilité** — IaC, conteneurs, configs versionnées.
4. **Sécurité** — chiffrement VPN, coffre de secrets, moindre privilège.
5. **Pédagogie** — technologies rencontrées en entreprise (Proxmox, pfSense, SIEM).

## Stack retenue

| Couche | Technologie | Version labo | Alternative écartée | Justification |
|--------|-------------|--------------|----------------------|---------------|
| Hyperviseur | Proxmox VE | 8.x | VMware ESXi | Open source, API Terraform, vzdump |
| Pare-feu | pfSense | 2.7.x | OPNsense | GUI mature, IPsec natif, CARP |
| VPN | IPsec (IKEv2) | pfSense natif | OpenVPN seul | Standard site-à-site, perf, intégration pfSense |
| VPN client | IPsec client-à-site | pfSense | WireGuard | Exigence sujet tunnel sécurisé inter-sites |
| IPAM | NetBox | 4.x | phpIPAM | API riche, DCIM, communauté NetDevOps |
| SIEM / logs | Wazuh | 4.x | Elastic SIEM | Agent léger, alertes intégrées, OSS |
| Secrets | HashiCorp Vault | 1.16+ | Ansible Vault seul | Rotation, policies, AppRole, Raft HA |
| Cache DB | Valkey | 7.x | Redis | Compatible Redis, licence OSS |
| BDD | PostgreSQL | 16.x | MySQL | Standard NetBox, sauvegardes pg_dump |
| IaC config | Ansible | Core 2.17 | Puppet/Chef | Agentless, YAML, intégration Vault |
| IaC provision | Terraform | 1.8+ | Pulumi | Provider Proxmox mature, déclaratif |
| Identité | Active Directory | 2022 | FreeIPA | PKI intégrée, LDAPS, DNS `mar2.local` |
| Accès distant | Apache Guacamole | 1.5.x | VPN seul | Bastion graphique, audit sessions |
| Reverse proxy | Nginx | 1.24+ | Traefik | Simple, TLS termination, léger |
| OS VMs | Ubuntu Server | 24.04 LTS | Debian | Cloud-Init, support Docker, LTS |
| Conteneurs | Docker CE + Compose | 24.x / v2 | Podman | Standard labo, Compose NetBox |

## Legacy (phase initiale, conservé dans le dépôt)

| Technologie | Raison du remplacement |
|-------------|------------------------|
| OpenVPN UDP 1194 | Remplacé par IPsec pour site-à-site (phase 2 labo) |
| Elastic Stack + Kibana | Remplacé par Wazuh (unification alertes + logs) |
| FluxCD / Kubernetes | Hors périmètre sujet Proxmox — archivé `legacy/` |

## Versions à documenter en soutenance (sans secrets)

Lister oralement ou sur slide :

```text
Proxmox VE 8.x · pfSense 2.7.x · Ubuntu 24.04 LTS
NetBox 4.x · Vault 1.16+ · Wazuh 4.x
Ansible 2.17 · Terraform 1.8+ · PostgreSQL 16
```

## Maintenance et mises à jour

| Composant | Fréquence | Méthode |
|-----------|-----------|---------|
| pfSense | Mensuelle | GUI System > Update |
| Proxmox | Trimestrielle | `apt update && apt dist-upgrade` |
| NetBox Docker | Mensuelle | `docker compose pull && up -d` |
| Vault | Selon CVE | Binaire + snapshot avant upgrade |
| Wazuh | Mensuelle | Manager + agents synchronisés |
| Ubuntu VMs | Hebdomadaire | `unattended-upgrades` (bastion, infraservice) |

## Références officielles

- [Proxmox VE Documentation](https://pve.proxmox.com/wiki/Main_Page)
- [pfSense Documentation](https://docs.netgate.com/)
- [NetBox Documentation](https://docs.netbox.dev/)
- [Wazuh Documentation](https://documentation.wazuh.com/)
- [HashiCorp Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [Ansible Documentation](https://docs.ansible.com/)
- [Terraform Proxmox Provider](https://registry.terraform.io/providers/Telmate/proxmox/latest/docs)
