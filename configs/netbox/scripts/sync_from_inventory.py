#!/usr/bin/env python3
"""
Synchronise sites, préfixes et adresses IP vers NetBox via API.
Usage:
  export NETBOX_URL=http://192.168.199.20:8080
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
    print("Installer: pip install -r configs/netbox/requirements.txt", file=sys.stderr)
    sys.exit(1)

DATA = Path(__file__).resolve().parents[1] / "sites-prefixes.example.yml"


class NetBoxClient:
    def __init__(self, base: str, token: str, dry_run: bool) -> None:
        self.base = base.rstrip("/")
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Token {token}", "Content-Type": "application/json"}
        )
        self._site_ids: dict[str, int] = {}

    def _post(self, path: str, payload: dict) -> dict | None:
        url = f"{self.base}{path}"
        if self.dry_run:
            print(f"[dry-run] POST {url} {payload}")
            return {"id": 0}
        r = self.session.post(url, json=payload, timeout=30)
        if r.status_code in (200, 201):
            return r.json()
        print(f"Erreur POST {path}: {r.status_code} {r.text}", file=sys.stderr)
        return None

    def _get_site_id(self, slug: str) -> int | None:
        if slug in self._site_ids:
            return self._site_ids[slug]
        if self.dry_run:
            self._site_ids[slug] = 0
            return 0
        r = self.session.get(
            f"{self.base}/api/dcim/sites/",
            params={"slug": slug},
            timeout=30,
        )
        if r.status_code == 200 and r.json().get("results"):
            sid = r.json()["results"][0]["id"]
            self._site_ids[slug] = sid
            return sid
        return None

    def ensure_site(self, site: dict) -> bool:
        slug = site["slug"]
        if self._get_site_id(slug) is not None:
            print(f"Site existant: {slug}")
            return True
        payload = {
            "name": site["name"],
            "slug": slug,
            "status": "active",
            "description": site.get("description", ""),
        }
        res = self._post("/api/dcim/sites/", payload)
        if res:
            self._site_ids[slug] = res.get("id", 0)
            print(f"OK site {slug}")
            return True
        return False

    def ensure_prefix(self, prefix: dict) -> bool:
        site_id = self._get_site_id(prefix["site"])
        payload = {
            "prefix": prefix["prefix"],
            "status": prefix.get("status", "active"),
            "description": prefix.get("description", ""),
        }
        if site_id is not None:
            payload["site"] = site_id
        res = self._post("/api/ipam/prefixes/", payload)
        if res:
            print(f"OK prefix {prefix['prefix']}")
            return True
        return False

    def ensure_ip(self, ip: dict) -> bool:
        payload = {
            "address": ip["address"],
            "status": "active",
            "description": ip.get("description", ""),
        }
        if ip.get("dns_name"):
            payload["dns_name"] = ip["dns_name"]
        res = self._post("/api/ipam/ip-addresses/", payload)
        if res:
            print(f"OK ip {ip['address']}")
            return True
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--file", type=Path, default=DATA)
    args = parser.parse_args()

    base = os.environ.get("NETBOX_URL", "").rstrip("/")
    token = os.environ.get("NETBOX_TOKEN", "")
    if not base or not token:
        print("Définir NETBOX_URL et NETBOX_TOKEN", file=sys.stderr)
        return 1

    data = yaml.safe_load(args.file.read_text())
    client = NetBoxClient(base, token, args.dry_run)

    ok = True
    for site in data.get("sites", []):
        ok = client.ensure_site(site) and ok
    for prefix in data.get("prefixes", []):
        ok = client.ensure_prefix(prefix) and ok
    for ip in data.get("ip_addresses", []):
        ok = client.ensure_ip(ip) and ok

    print("Synchronisation terminée." if ok else "Erreurs — voir ci-dessus.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
