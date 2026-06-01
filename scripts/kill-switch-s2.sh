#!/usr/bin/env bash
# Kill switch réversible — Site 2 OpenVPN (pfSense)
# Usage:
#   ./scripts/kill-switch-s2.sh off    # couper VPN entrant
#   ./scripts/kill-switch-s2.sh on     # rétablir (rollback)
#   ./scripts/kill-switch-s2.sh status # vérifier port 1194 depuis Internet
set -euo pipefail

PFSENSE_HOST="${PFSENSE_HOST:-192.168.10.1}"
PFSENSE_SSH_USER="${PFSENSE_SSH_USER:-admin}"
PUBLIC_IP="${PUBLIC_IP:-78.202.114.212}"
VPN_PORT=1194

status() {
  echo "=== Test UDP $VPN_PORT sur $PUBLIC_IP ==="
  nc -vzu -G 5 "$PUBLIC_IP" "$VPN_PORT" || true
  echo "=== Test ping LAN via VPN (si connecté) ==="
  ping -c 2 -W 2 192.168.102.11 || true
}

case "${1:-status}" in
  off)
    echo "MANUEL pfSense: Firewall > Rules > WAN — désactiver règle UDP $VPN_PORT"
    echo "Puis: Apply Changes"
    echo "Ou SSH (si activé sur pfSense):"
    echo "  ssh ${PFSENSE_SSH_USER}@${PFSENSE_HOST}"
    echo "  pfctl -d  # DANGER: désactive tout le filtrage — préférer GUI"
    status
    ;;
  on)
    echo "MANUEL pfSense: réactiver règle UDP $VPN_PORT + Apply"
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
