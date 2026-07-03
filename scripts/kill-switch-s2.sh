#!/usr/bin/env bash
# Kill switch réversible — Site 2 (pfSense, VPN IPsec)
# Usage:
#   ./scripts/kill-switch-s2.sh off    # couper VPN entrant
#   ./scripts/kill-switch-s2.sh on     # rétablir (rollback)
#   ./scripts/kill-switch-s2.sh status # vérifier reachabilité LAN via VPN
set -euo pipefail

PFSENSE_HOST="${PFSENSE_HOST:-192.168.10.1}"
PFSENSE_SSH_USER="${PFSENSE_SSH_USER:-admin}"
PUBLIC_IP="${PUBLIC_IP:-78.202.114.212}"
INFRASERVICE_IP="${INFRASERVICE_IP:-192.168.10.15}"

status() {
  echo "=== Test ping Proxmox S2 via VPN (si connecté) ==="
  ping -c 2 -W 2 192.168.102.11 || true
  echo "=== Test ping InfraService via VPN (si connecté) ==="
  ping -c 2 -W 2 "$INFRASERVICE_IP" || true
  echo "=== Test SSH bastion public (port 2222) ==="
  nc -vz -G 5 "$PUBLIC_IP" 2222 || true
}

case "${1:-status}" in
  off)
    echo "MANUEL pfSense: VPN > IPsec — désactiver tunnel phase 1/2"
    echo "Ou: Firewall > Rules > WAN — désactiver règle IPsec associée"
    echo "Puis: Apply Changes"
    echo "Legacy OpenVPN (phase 1): désactiver règle UDP 1194 si encore active"
    status
    ;;
  on)
    echo "MANUEL pfSense: réactiver tunnel IPsec + Apply"
    status
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 {off|on|status}"
    exit 1
    ;;
esac
