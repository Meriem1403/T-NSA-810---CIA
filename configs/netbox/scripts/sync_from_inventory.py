#!/usr/bin/env python3
"""
Synchronise préfixes / IP vers NetBox via API.
Usage:
  export NETBOX_URL=https://netbox.example.local
  export NETBOX_TOKEN=...
  python3 sync_from_inventory.py [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

try:
    import requests
    import yaml
except ImportError:
    print("Installer: pip install requests pyyaml", file=sys.stderr)
    sys.exit(1)

DATA = Path(__file__).resolve().parents[1] / "sites-prefixes.example.yml"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Afficher sans POST")
    parser.add_argument("--file", type=Path, default=DATA)
    args = parser.parse_args()

    base = os.environ.get("NETBOX_URL", "").rstrip("/")
    token = os.environ.get("NETBOX_TOKEN", "")
    if not base or not token:
        print("Définir NETBOX_URL et NETBOX_TOKEN", file=sys.stderr)
        return 1

    data = yaml.safe_load(args.file.read_text())
    headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}
    session = requests.Session()
    session.headers.update(headers)

    for prefix in data.get("prefixes", []):
        payload = {
            "prefix": prefix["prefix"],
            "status": prefix.get("status", "active"),
            "description": prefix.get("description", ""),
        }
        if args.dry_run:
            print(f"[dry-run] POST {base}/api/ipam/prefixes/ {payload}")
            continue
        r = session.post(f"{base}/api/ipam/prefixes/", json=payload, timeout=30)
        if r.status_code not in (200, 201):
            print(f"Erreur prefix {prefix['prefix']}: {r.status_code} {r.text}", file=sys.stderr)
            return 1
        print(f"OK prefix {prefix['prefix']}")

    print("Synchronisation terminée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
