#!/usr/bin/env python3
"""Génère une présentation PowerPoint détaillée et soignée pour la soutenance CIA."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
OUT_DIR = DOCS / "presentations"
OUT_ROOT = ROOT / "CIA-Soutenance.pptx"
DIAGRAM = DOCS / "architecture-diagram.png"

# ── Palette ──────────────────────────────────────────────────────────────
NAVY = RGBColor(0x0B, 0x1D, 0x33)
NAVY_MID = RGBColor(0x14, 0x3D, 0x5C)
TEAL = RGBColor(0x00, 0xB4, 0xA0)
TEAL_DARK = RGBColor(0x00, 0x8F, 0x7F)
ACCENT = RGBColor(0xFF, 0x6B, 0x35)
GOLD = RGBColor(0xF4, 0xA2, 0x61)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OFF_WHITE = RGBColor(0xF7, 0xF9, 0xFC)
LIGHT_GRAY = RGBColor(0xE2, 0xE8, 0xF0)
TEXT = RGBColor(0x1E, 0x29, 0x3B)
TEXT_SOFT = RGBColor(0x64, 0x74, 0x8B)
SUCCESS = RGBColor(0x10, 0xB9, 0x81)
ROW_ALT = RGBColor(0xF1, 0xF5, 0xF9)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


class Deck:
  def __init__(self) -> None:
    self.prs = Presentation()
    self.prs.slide_width = SLIDE_W
    self.prs.slide_height = SLIDE_H
    self._n = 0

  def _blank(self):
    self._n += 1
    return self.prs.slides.add_slide(self.prs.slide_layouts[6])

  @staticmethod
  def _bg(slide, color: RGBColor) -> None:
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = color

  def _accent_bar(self, slide) -> None:
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.18), SLIDE_H)
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()

  def _header(self, slide, title: str, subtitle: str = "") -> None:
    self._bg(slide, OFF_WHITE)
    self._accent_bar(slide)
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.18), 0, SLIDE_W, Inches(1.35))
    band.fill.solid()
    band.fill.fore_color.rgb = NAVY
    band.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.22), Inches(10.5), Inches(0.65))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = WHITE

    if subtitle:
      sb = slide.shapes.add_textbox(Inches(0.55), Inches(0.82), Inches(11), Inches(0.4))
      sp = sb.text_frame.paragraphs[0]
      sp.text = subtitle
      sp.font.size = Pt(13)
      sp.font.color.rgb = TEAL

    num = slide.shapes.add_textbox(SLIDE_W - Inches(0.9), Inches(0.35), Inches(0.6), Inches(0.4))
    np = num.text_frame.paragraphs[0]
    np.text = str(self._n)
    np.font.size = Pt(11)
    np.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    np.alignment = PP_ALIGN.RIGHT

  def _footer(self, slide, tag: str = "") -> None:
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.18), SLIDE_H - Inches(0.38), SLIDE_W, Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL
    line.line.fill.background()
    txt = f"T-NSA-810 · CIA · Meriem ZAHZOUH & Kévin SEMERCIYAN"
    if tag:
      txt += f"  ·  {tag}"
    box = slide.shapes.add_textbox(Inches(0.55), SLIDE_H - Inches(0.35), Inches(12), Inches(0.28))
    box.text_frame.paragraphs[0].text = txt
    box.text_frame.paragraphs[0].font.size = Pt(9)
    box.text_frame.paragraphs[0].font.color.rgb = TEXT_SOFT

  def _bullets(self, slide, items: list[tuple[str, str]], left: float, top: float, width: float, height: float) -> None:
    """items = [(label, detail), ...] ou [(text, ''), ...]"""
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, (label, detail) in enumerate(items):
      para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
      if detail:
        para.text = f"▸  {label}"
        para.font.size = Pt(14)
        para.font.bold = True
        para.font.color.rgb = NAVY
        para.space_after = Pt(2)
        sub = tf.add_paragraph()
        sub.text = f"     {detail}"
        sub.font.size = Pt(12)
        sub.font.color.rgb = TEXT_SOFT
        sub.space_after = Pt(10)
      else:
        para.text = f"▸  {label}"
        para.font.size = Pt(13)
        para.font.color.rgb = TEXT
        para.space_after = Pt(8)

  def _card(self, slide, x: float, y: float, w: float, h: float, title: str, body: str, color: RGBColor = NAVY_MID) -> None:
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid()
    card.fill.fore_color.rgb = color
    card.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.12), Inches(w - 0.3), Inches(h - 0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL
    p1 = tf.add_paragraph()
    p1.text = body
    p1.font.size = Pt(11)
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(6)

  def _stat(self, slide, x: float, label: str, value: str, sub: str = "") -> None:
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.55), Inches(2.6), Inches(1.5))
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = LIGHT_GRAY
    card.line.width = Pt(1)
    v = slide.shapes.add_textbox(Inches(x + 0.15), Inches(1.7), Inches(2.3), Inches(0.7))
    v.text_frame.paragraphs[0].text = value
    v.text_frame.paragraphs[0].font.size = Pt(32)
    v.text_frame.paragraphs[0].font.bold = True
    v.text_frame.paragraphs[0].font.color.rgb = TEAL
    l = slide.shapes.add_textbox(Inches(x + 0.15), Inches(2.35), Inches(2.3), Inches(0.35))
    l.text_frame.paragraphs[0].text = label
    l.text_frame.paragraphs[0].font.size = Pt(11)
    l.text_frame.paragraphs[0].font.bold = True
    l.text_frame.paragraphs[0].font.color.rgb = NAVY
    if sub:
      s = slide.shapes.add_textbox(Inches(x + 0.15), Inches(2.65), Inches(2.3), Inches(0.35))
      s.text_frame.paragraphs[0].text = sub
      s.text_frame.paragraphs[0].font.size = Pt(9)
      s.text_frame.paragraphs[0].font.color.rgb = TEXT_SOFT

  def _table(self, slide, headers: list[str], rows: list[list[str]], top: float = 1.55, col_widths: list[float] | None = None) -> None:
    nrows, ncols = len(rows) + 1, len(headers)
    tbl = slide.shapes.add_table(nrows, ncols, Inches(0.55), Inches(top), Inches(12.2), Inches(min(0.42 * nrows, 5.2))).table
    if col_widths:
      for i, w in enumerate(col_widths):
        tbl.columns[i].width = Inches(w)
    for c, h in enumerate(headers):
      cell = tbl.cell(0, c)
      cell.text = h
      cell.fill.solid()
      cell.fill.fore_color.rgb = NAVY
      for p in cell.text_frame.paragraphs:
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
    for r, row in enumerate(rows, 1):
      for c, val in enumerate(row):
        cell = tbl.cell(r, c)
        cell.text = val
        if r % 2 == 0:
          cell.fill.solid()
          cell.fill.fore_color.rgb = ROW_ALT
        for p in cell.text_frame.paragraphs:
          p.font.size = Pt(10)
          p.font.color.rgb = TEXT

  # ── Slides ─────────────────────────────────────────────────────────────

  def slide_cover(self) -> None:
    s = self._blank()
    self._bg(s, NAVY)
    # Décor
    deco = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(9.5), Inches(-0.5), Inches(5), Inches(3))
    deco.fill.solid()
    deco.fill.fore_color.rgb = NAVY_MID
    deco.line.fill.background()
    stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(6.8), SLIDE_W, Inches(0.7))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = TEAL
    stripe.line.fill.background()

    t = s.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(8), Inches(1.2))
    t.text_frame.paragraphs[0].text = "T-NSA-810"
    t.text_frame.paragraphs[0].font.size = Pt(20)
    t.text_frame.paragraphs[0].font.color.rgb = TEAL

    t2 = s.shapes.add_textbox(Inches(0.9), Inches(2.3), Inches(10), Inches(1.4))
    t2.text_frame.paragraphs[0].text = "Cloud Infrastructure\nArchitects (CIA)"
    t2.text_frame.paragraphs[0].font.size = Pt(48)
    t2.text_frame.paragraphs[0].font.bold = True
    t2.text_frame.paragraphs[0].font.color.rgb = WHITE

    sub = s.shapes.add_textbox(Inches(0.9), Inches(4.0), Inches(9), Inches(0.9))
    sub.text_frame.paragraphs[0].text = "Infrastructure hybride sécurisée · Proxmox · pfSense · IPsec"
    sub.text_frame.paragraphs[0].font.size = Pt(18)
    sub.text_frame.paragraphs[0].font.color.rgb = GOLD

    team = s.shapes.add_textbox(Inches(0.9), Inches(5.2), Inches(8), Inches(1))
    team.text_frame.paragraphs[0].text = "Meriem ZAHZOUH  ·  Kévin SEMERCIYAN"
    team.text_frame.paragraphs[0].font.size = Pt(16)
    team.text_frame.paragraphs[0].font.color.rgb = LIGHT_GRAY
    team.text_frame.add_paragraph().text = f"Epitech Master 2 NSA  ·  {date.today().strftime('%d/%m/%Y')}"
    team.text_frame.paragraphs[1].font.size = Pt(12)
    team.text_frame.paragraphs[1].font.color.rgb = TEXT_SOFT

  def slide_agenda(self) -> None:
    s = self._blank()
    self._header(s, "Plan de la soutenance", "~20 minutes · démo live incluse")
    items = [
      ("01", "Contexte & problématique du sujet"),
      ("02", "Ce que nous avons réalisé — vue d'ensemble"),
      ("03", "Architecture & réseau (2 sites Proxmox)"),
      ("04", "Sécurité : bastion, pare-feu, Vault"),
      ("05", "Services : NetBox, Wazuh, Guacamole"),
      ("06", "Automatisation IaC : Ansible & Terraform"),
      ("07", "Incident : kill switch & reprise (DRP)"),
      ("08", "Dépôt Git, planning & démonstration live"),
    ]
    for i, (num, text) in enumerate(items):
      col, row = i % 2, i // 2
      x = 0.55 + col * 6.3
      y = 1.65 + row * 1.35
      badge = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.55), Inches(0.55))
      badge.fill.solid()
      badge.fill.fore_color.rgb = TEAL if i % 2 == 0 else ACCENT
      badge.line.fill.background()
      nb = s.shapes.add_textbox(Inches(x), Inches(y + 0.1), Inches(0.55), Inches(0.4))
      nb.text_frame.paragraphs[0].text = num
      nb.text_frame.paragraphs[0].font.size = Pt(12)
      nb.text_frame.paragraphs[0].font.bold = True
      nb.text_frame.paragraphs[0].font.color.rgb = WHITE
      nb.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
      tx = s.shapes.add_textbox(Inches(x + 0.7), Inches(y + 0.12), Inches(5.4), Inches(0.5))
      tx.text_frame.paragraphs[0].text = text
      tx.text_frame.paragraphs[0].font.size = Pt(14)
      tx.text_frame.paragraphs[0].font.color.rgb = TEXT
    self._footer(s)

  def slide_problem(self) -> None:
    s = self._blank()
    self._header(s, "Le sujet : qu'est-ce qu'on devait livrer ?", "T-NSA-810 — Cloud Infrastructure Architects")
    self._card(s, 0.55, 1.55, 3.8, 2.4, "🎯 Objectif",
               "Construire une infrastructure hybride réelle : 2 sites Proxmox reliés par VPN, sécurisés, observable et reproductible par IaC.", NAVY_MID)
    self._card(s, 4.55, 1.55, 3.8, 2.4, "📋 Contraintes",
               "Max 3 VMs/site · Stack open source · Aucun secret dans Git · Site web interne uniquement · Kill switch réversible.", NAVY)
    self._card(s, 8.55, 1.55, 3.8, 2.4, "✅ Résultat",
               "90 % d'avancement · Labo opérationnel · 29 trophées documentés · Dépôt GitHub complet.", TEAL_DARK)
    self._bullets(s, [
      ("Deux mondes à relier", "Site on-prem (S1) + site distant sur Internet (S2) avec routage sécurisé"),
      ("Zéro confiance périmétrique", "Pare-feu des deux côtés, bastion, pas d'exposition HTTP/SSH0 directe"),
      ("Tout doit être rejouable", "Ansible, Terraform, configs versionnées, procédure DRP écrite"),
    ], 0.55, 4.2, 11.8, 2.5)
    self._footer(s, "infra_spec · infra_delivery")

  def slide_stats(self) -> None:
    s = self._blank()
    self._header(s, "Bilan du projet", "État au 23 juin 2026 — docs/status-2026-06-23.md")
    self._stat(s, 0.55, "Avancement global", "90 %", "12 phases sur 13 avancées")
    self._stat(s, 3.45, "Composants OK", "15/19", "Proxmox, VPN, NetBox, Vault…")
    self._stat(s, 6.35, "Documentation", "25+", "fichiers docs/ + configs/")
    self._stat(s, 9.25, "Trophées Epitech", "29", "guide de validation complet")
    self._table(s, ["Composant", "État", "Ce qu'on a fait"],
      [
        ["Proxmox 01 & 02", "✅ 100 %", "2 hyperviseurs, VMs, bridges, stockage"],
        ["pfSense + CARP", "✅ 100 %", "2 pare-feu, NAT, règles WAN/LAN documentées"],
        ["VPN IPsec", "✅ 100 %", "Site-à-site + client-à-site, tunnel UP"],
        ["NetBox + PostgreSQL", "✅ 100 %", "Docker sur infraservice, sync API Ansible"],
        ["Vault", "✅ 100 %", "Raft, KV v2, AppRole Ansible, snapshots"],
        ["Wazuh", "🟡 90 %", "Manager + agents, dashboards à finaliser"],
        ["Terraform", "🟡 70 %", "init/validate/plan OK, apply en attente template"],
        ["Kill Switch", "🟡 30 %", "Script + runbook, test chrono à faire"],
      ], top=3.3, col_widths=[2.8, 1.2, 8.2])
    self._footer(s, "proj_planning")

  def slide_timeline(self) -> None:
    s = self._blank()
    self._header(s, "Notre parcours — les grandes phases", "De zéro à une infra hybride démontrable")
    phases = [
      ("F0–F1", "Cadrage", "Repo Git, README, diagramme, grille évaluation"),
      ("F2–F3", "Fondations", "Proxmox, pfSense, segmentation réseau S1/S2"),
      ("F4", "VPN", "IPsec site-à-site + accès client distant"),
      ("F5", "Identité", "AD mar2.local, DNS, Guacamole, bastion SSH"),
      ("F7–F8", "Services", "InfraService : NetBox, Vault, Ansible"),
      ("F6", "Supervision", "Wazuh manager + agents sur les VMs"),
      ("F9", "Terraform", "Provider Proxmox, plan validé"),
      ("F11", "Soutenance", "Doc 29 trophées, slides, démo live"),
    ]
    for i, (code, name, desc) in enumerate(phases):
      x = 0.55 + (i % 4) * 3.1
      y = 1.6 + (i // 4) * 2.5
      self._card(s, x, y, 2.85, 2.1, f"{code}  {name}", desc, NAVY_MID if i % 2 == 0 else NAVY)
    self._footer(s)

  def slide_team(self) -> None:
    s = self._blank()
    self._header(s, "Répartition du travail", "Qui a fait quoi dans l'équipe")
    self._card(s, 0.55, 1.55, 5.9, 5.0,
               "Meriem ZAHZOUH — Infra S2 & documentation",
               "• Restructuration du dépôt pour le livrable CIA (Proxmox)\n"
               "• Déploiement site distant : VMs pfSense, bastion, client Windows\n"
               "• Site interne nginx (192.168.10.11) — accessible LAN/VPN seulement\n"
               "• Scénarios de démo : VPN, bastion, pare-feu, DNS\n"
               "• Règles pfSense S2, script kill-switch-s2.sh\n"
               "• Harmonisation doc + guide 29 trophées + grille Excel\n"
               "• Rôle Ansible bastion (déploiement nginx automatisé)", NAVY)
    self._card(s, 6.75, 1.55, 5.9, 5.0,
               "Kévin SEMERCIYAN — Services & IaC",
               "• Plateforme InfraService (192.168.10.15) : Docker, NetBox, Vault\n"
               "• Wazuh : manager + agents, collecte centralisée des logs\n"
               "• Ansible Core 2.17 : playbooks, inventaire, rôles modulaires\n"
               "• Intégration Vault AppRole (lecture secrets validée)\n"
               "• Terraform : provider Proxmox, init/validate/plan\n"
               "• AD mar2.local, Guacamole, pfSense S1\n"
               "• Gantt F0–F11, status d'avancement, planning", TEAL_DARK)
    self._footer(s, "proj_subdivision")

  def slide_architecture(self) -> None:
    s = self._blank()
    self._header(s, "Architecture globale", "Deux sites reliés par tunnel IPsec · domaine mar2.local")
    if DIAGRAM.exists():
      frame = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), Inches(1.45), Inches(8.3), Inches(5.5))
      frame.fill.solid()
      frame.fill.fore_color.rgb = WHITE
      frame.line.color.rgb = TEAL
      frame.line.width = Pt(2)
      s.shapes.add_picture(str(DIAGRAM), Inches(0.6), Inches(1.6), width=Inches(8.0))
    self._card(s, 9.0, 1.55, 3.6, 1.3, "Site 1 — On-prem", "Proxmox 02 · pfSense\nAD mar2.local · LAN .199.0/24", NAVY)
    self._card(s, 9.0, 3.05, 3.6, 1.3, "Site 2 — Remote", "Proxmox 01 · IP publique\npfSense CARP · LAN .10.0/24", NAVY_MID)
    self._card(s, 9.0, 4.55, 3.6, 1.3, "InfraService", "192.168.10.15\nNetBox · Vault · Wazuh", TEAL_DARK)
    self._card(s, 9.0, 6.05, 3.6, 0.85, "VPN IPsec", "S1 ↔ S2 + client distant", ACCENT)
    self._footer(s, "diagram_delivery · diagram_quality")

  def slide_site2_detail(self) -> None:
    s = self._blank()
    self._header(s, "Site 2 — ce qu'on a déployé concrètement", "Proxmox-01 · IP publique 78.202.114.212")
    self._table(s, ["VM", "IP", "Ce qu'on a configuré", "Preuve"],
      [
        ["pfSense VM100", "WAN .102.103\nLAN .10.1", "Interfaces WAN/LAN, NAT 2222→bastion, règles IPsec, DNS overrides", "GUI pfSense + nc port 2222"],
        ["Client VM101", "192.168.10.10", "Poste Windows interne pour tests DNS et reachability", "ping depuis bastion"],
        ["Bastion VM102", "192.168.10.11", "Ubuntu, SSH durci, nginx + page interne, compte bastion", "ssh -p 2222 + curl HTTP 200"],
        ["InfraService", "192.168.10.15", "Docker NetBox, Vault Raft, Wazuh, Ansible, Terraform", "curl :8000 et :8200"],
      ], col_widths=[1.8, 1.8, 5.2, 3.4])
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(5.0), Inches(12.2), Inches(1.5))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0xFF, 0xF7, 0xED)
    box.line.color.rgb = ACCENT
    box.line.width = Pt(1)
    note = s.shapes.add_textbox(Inches(0.75), Inches(5.15), Inches(11.8), Inches(1.2))
    note.text_frame.paragraphs[0].text = "💡 Choix labo : services regroupés sur infraservice pour respecter la contrainte 3 VMs/site Proxmox"
    note.text_frame.paragraphs[0].font.size = Pt(13)
    note.text_frame.paragraphs[0].font.bold = True
    note.text_frame.paragraphs[0].font.color.rgb = ACCENT
    note.text_frame.add_paragraph().text = "Évolution documentée : OpenVPN (phase 1) → IPsec (production) · ELK → Wazuh"
    note.text_frame.paragraphs[1].font.size = Pt(12)
    note.text_frame.paragraphs[1].font.color.rgb = TEXT_SOFT
    self._footer(s, "network_spec2 · infra_delivery")

  def slide_vpn(self) -> None:
    s = self._blank()
    self._header(s, "VPN IPsec — notre réalisation", "Tunnel site-à-site + accès client distant opérationnels")
    self._bullets(s, [
      ("Phase 1 — OpenVPN (début de projet)", "UDP 1194, réseau 10.8.0.0/24 — preuves initiales conservées dans le dépôt"),
      ("Phase 2 — IPsec (état actuel)", "IKEv2 sur pfSense, ports UDP 500/4500 + ESP, tunnel S1 ↔ S2 stable"),
      ("Configuration réalisée", "Phase 1 & 2 IPsec sur les deux pfSense, PSK/certificats stockés dans Vault (hors Git)"),
      ("Tests validés", "ping 192.168.10.15 depuis Mac connecté · traceroute via tunnel · statut UP dans pfSense"),
      ("Sécurité", "Aucun accès LAN sans tunnel — kill switch = désactiver Phase 1 en < 10 min"),
    ], 0.55, 1.55, 6.0, 5.2)
    self._card(s, 6.8, 1.55, 5.8, 2.2, "Commandes de démo", "ping -c 3 192.168.10.15\ntraceroute 192.168.10.15\npfSense → VPN → IPsec → Status", NAVY_MID)
    self._card(s, 6.8, 4.0, 5.8, 2.5, "Avant → Après", "AVANT : accès direct impossible\npendant le dev local\n\nAPRÈS : tunnel chiffré,\nroutage inter-sites, admin\nà distance sécurisée", TEAL_DARK)
    self._footer(s, "network_vpn")

  def slide_firewall_bastion(self) -> None:
    s = self._blank()
    self._header(s, "Pare-feu & bastion — sécurité périmétrique", "Moindre privilège · un seul point d'entrée SSH contrôlé")
    self._table(s, ["Test", "Commande", "Résultat attendu", "Statut"],
      [
        ["SSH port 22 public", "nc -vz 78.202.114.212 22", "Timeout / refus", "✅ Validé"],
        ["SSH bastion 2222", "nc -vz 78.202.114.212 2222", "Connexion OK", "✅ Validé"],
        ["HTTP public", "curl -I http://78.202.114.212", "Timeout", "✅ Validé"],
        ["Site interne via VPN", "curl -I http://192.168.10.11", "HTTP 200 OK", "✅ Validé"],
        ["IPsec WAN", "Tunnel pfSense Status", "UP", "✅ Validé"],
      ], top=1.55, col_widths=[2.5, 3.5, 2.8, 1.2])
    self._bullets(s, [
      ("Bastion Ubuntu VM102", "Compte dédié bastion, PermitRootLogin prohibit-password, nginx site CIA"),
      ("Guacamole", "Accès graphique centralisé depuis LAN/VPN — sessions auditables"),
      ("Documentation", "configs/pfsense/site1 + site2, demo-scenarios.md § B C D"),
    ], 0.55, 4.5, 12.0, 2.2)
    self._footer(s, "network_firewall · sec_bastion · sec_access")

  def slide_infraservice(self) -> None:
    s = self._blank()
    self._header(s, "Plateforme InfraService", "192.168.10.15 — cœur des services d'administration")
    services = [
      ("NetBox :8000", "IPAM/DCIM Docker\nPostgreSQL + Valkey\nSync API Ansible"),
      ("Vault :8200", "Raft intégré · KV v2\nAppRole Ansible\nSnapshots auto"),
      ("Wazuh", "Manager SIEM\nAgents sur bastion\nAlertes sécurité"),
      ("Ansible 2.17", "Playbooks + rôles\nInventaire structuré\nLecture Vault OK"),
      ("Terraform", "Provider Proxmox\nterraform plan OK\napply → template CI"),
      ("Guacamole", "Bastion graphique\nAccès LAN/VPN\nDurcissement en cours"),
    ]
    for i, (title, body) in enumerate(services):
      x = 0.55 + (i % 3) * 4.15
      y = 1.55 + (i // 3) * 2.55
      colors = [NAVY, NAVY_MID, TEAL_DARK, NAVY_MID, NAVY, TEAL_DARK]
      self._card(s, x, y, 3.85, 2.25, title, body, colors[i])
    self._footer(s, "infra_delivery · network_ip_mngmt · sec_credentials")

  def slide_netbox_vault(self) -> None:
    s = self._blank()
    self._header(s, "NetBox & Vault — ce qu'on a automatisé", "IPAM vivant + secrets centralisés")
    self._card(s, 0.55, 1.55, 5.9, 4.8, "NetBox — IPAM",
               "✓ Déployé en Docker Compose sur infraservice\n"
               "✓ Sites site1 / site2 et préfixes RFC1918 modélisés\n"
               "✓ Script Python sync_from_inventory.py\n"
               "✓ Playbook ansible netbox-sync.yml\n"
               "✓ Token API dans Vault (jamais dans Git)\n"
               "→ À finaliser : inventaire complet VMs/équipements", NAVY_MID)
    self._card(s, 6.75, 1.55, 5.9, 4.8, "HashiCorp Vault",
               "✓ Installé avec stockage Raft intégré\n"
               "✓ Init, unseal, moteur KV v2 sur infra/\n"
               "✓ Policies + AppRole dédié Ansible\n"
               "✓ Collection community.hashi_vault\n"
               "✓ Lecture secret validée en labo\n"
               "✓ Sauvegardes Raft automatiques", TEAL_DARK)
    self._footer(s, "network_ip_mngmt · sec_credentials · iac_quality")

  def slide_wazuh(self) -> None:
    s = self._blank()
    self._header(s, "Wazuh — observabilité & logs centralisés", "Remplacement de la stack ELK initiale")
    self._bullets(s, [
      ("Pourquoi Wazuh ?", "Agent léger, alertes intégrées, SIEM open source adapté au labo"),
      ("Ce qu'on a déployé", "Manager sur infraservice, agents sur bastion et hôtes supervisés"),
      ("Logs collectés", "auth.log SSH, syslog système, événements sécurité, intégrité fichiers"),
      ("Test validé", "logger 'CIA-WAZUH-TEST' visible dans l'interface < 2 minutes"),
      ("Reste à faire", "Dashboards finaux, alertes brute-force SSH, capture pour soutenance"),
    ], 0.55, 1.55, 6.2, 4.5)
    self._card(s, 7.0, 1.55, 5.5, 2.0, "Évolution projet", "Phase 1 : Elastic + Kibana\n+ Filebeat sur bastion\n\nPhase 2 : Wazuh\n(unification alertes + logs)", NAVY)
    self._card(s, 7.0, 3.8, 5.5, 2.3, "Trophées couverts", "log_centralisation\nlog_observability\nlog_analysis\nlog_visuals", TEAL_DARK)
    self._footer(s, "log_*")

  def slide_iac(self) -> None:
    s = self._blank()
    self._header(s, "Infrastructure as Code", "Ansible + Terraform — reproduire le labo depuis Git")
    self._card(s, 0.55, 1.55, 6.0, 5.2, "Ansible — configuration",
               "Playbooks :\n"
               "  • site.yml → baseline + bastion nginx\n"
               "  • deploy-site1.yml → Docker NetBox/Elastic\n"
               "  • netbox-sync.yml → sync IPAM API\n"
               "  • deploy-observability.yml → Filebeat (legacy)\n\n"
               "Rôles : bastion, docker_host, netbox_stack,\n"
               "elastic_stack, filebeat, netbox_sync\n\n"
               "✓ Inventaire example.inventory.yml\n"
               "✓ Intégration Vault AppRole validée", NAVY_MID)
    self._card(s, 6.85, 1.55, 5.8, 5.2, "Terraform — provisionnement",
               "Provider telmate/proxmox\n\n"
               "✓ terraform init\n"
               "✓ terraform validate\n"
               "✓ terraform plan (API Proxmox OK)\n\n"
               "Module VM Cloud-Init Ubuntu\n"
               "Variables typées + tfvars.example\n"
               "État .tfstate hors Git\n\n"
               "⏳ Bloqué : template ubuntu-template\n"
               "→ Chaîne : TF apply → Ansible", TEAL_DARK)
    self._footer(s, "iac_delivery · iac_quality")

  def slide_kill_drp(self) -> None:
    s = self._blank()
    self._header(s, "Kill switch & reprise après sinistre", "Couper vite · revenir en arrière · reconstruire dans l'ordre")
    self._bullets(s, [
      ("Kill switch réalisé", "Script scripts/kill-switch-s2.sh + procédure drp-runbook.md"),
      ("Action de coupure", "Désactiver tunnel IPsec Phase 1 sur pfSense S2 → ping LAN échoue"),
      ("Rollback", "Réactiver tunnel + Apply → ping OK en < 10 minutes (objectif soutenance)"),
      ("DRP — ordre reconstruction", "Proxmox → réseau → pfSense → VPN → Vault → NetBox → Wazuh → bastion"),
      ("Sauvegardes", "Vault Raft snapshots OK · NetBox/PostgreSQL à industrialiser"),
      ("Évolution", "API Kill Switch + déclenchement depuis alertes Wazuh"),
    ], 0.55, 1.55, 7.5, 5.3)
    self._card(s, 8.3, 1.55, 4.3, 5.2, "Checklist post-rebuild",
               "☐ Tunnel IPsec UP\n"
               "☐ DNS mar2.local OK\n"
               "☐ NetBox accessible\n"
               "☐ Vault unsealed\n"
               "☐ Agents Wazuh actifs\n"
               "☐ Site interne non exposé\n"
               "☐ SSH via bastion :2222", NAVY)
    self._footer(s, "incident_killswitch · incident_recovery")

  def slide_git(self) -> None:
    s = self._blank()
    self._header(s, "Dépôt GitHub & documentation", "github.com/Meriem1403/T-NSA-810---CIA")
    self._table(s, ["Dossier", "Contenu livré", "Fichiers clés"],
      [
        ["docs/", "25+ guides", "architecture, trophees-validation, demo-scenarios, gantt"],
        ["configs/", "Réseau & services", "pfsense/, dns/, netbox/, wazuh/"],
        ["iac/ansible/", "Automatisation CM", "4 playbooks, 8 rôles, inventaire"],
        ["iac/terraform/", "Provisionnement", "main.tf, variables, provider Proxmox"],
        ["apps/", "Site interne", "internal-site/index.html + nginx"],
        ["scripts/", "Outils", "kill-switch-s2.sh, generate_presentation.py"],
      ], top=1.55, col_widths=[2.0, 2.5, 7.7])
    self._bullets(s, [
      ("Workflow Git", "Branches feature/ + PR avec tests manuels · commits conventionnels · .gitignore strict"),
      ("29 trophées", "docs/trophees-validation.md — chaque trophée mappé vers un livrable et une preuve"),
      ("Legacy archivé", "Flux/Kubernetes sous legacy/flux-bootstrap/ — hors périmètre sujet"),
    ], 0.55, 4.6, 12.0, 2.0)
    self._footer(s, "repo_practices · repo_doc · repo_content")

  def slide_demo(self) -> None:
    s = self._blank()
    self._header(s, "Démonstration live", "Commandes à exécuter pendant la soutenance")
    cmds = [
      ("1. VPN", "ping -c 2 192.168.10.15"),
      ("2. Site interne", "curl -I http://192.168.10.11"),
      ("3. Bastion SSH", "ssh -p 2222 bastion@78.202.114.212"),
      ("4. Pare-feu", "nc -vz 78.202.114.212 22  # KO"),
      ("5. DNS", "nslookup client1.site2.local 192.168.10.1"),
      ("6. NetBox", "curl -I http://192.168.10.15:8000"),
      ("7. Logs Wazuh", "logger 'CIA-SOUTENANCE-TEST'"),
      ("8. IaC", "cd iac/terraform && terraform plan"),
    ]
    for i, (label, cmd) in enumerate(cmds):
      col, row = i % 2, i // 2
      x = 0.55 + col * 6.3
      y = 1.55 + row * 1.35
      card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(5.9), Inches(1.15))
      card.fill.solid()
      card.fill.fore_color.rgb = WHITE
      card.line.color.rgb = TEAL
      card.line.width = Pt(1.5)
      lb = s.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.1), Inches(5.6), Inches(0.35))
      lb.text_frame.paragraphs[0].text = label
      lb.text_frame.paragraphs[0].font.size = Pt(12)
      lb.text_frame.paragraphs[0].font.bold = True
      lb.text_frame.paragraphs[0].font.color.rgb = TEAL
      cm = s.shapes.add_textbox(Inches(x + 0.15), Inches(y + 0.45), Inches(5.6), Inches(0.55))
      cm.text_frame.paragraphs[0].text = cmd
      cm.text_frame.paragraphs[0].font.size = Pt(11)
      cm.text_frame.paragraphs[0].font.name = "Courier New"
      cm.text_frame.paragraphs[0].font.color.rgb = NAVY
    self._footer(s, "proj_presentation")

  def slide_conclusion(self) -> None:
    s = self._blank()
    self._bg(s, NAVY)
    stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(3.2), SLIDE_W, Inches(0.08))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = TEAL
    stripe.line.fill.background()

    t = s.shapes.add_textbox(Inches(0.9), Inches(1.5), Inches(11), Inches(1.2))
    t.text_frame.paragraphs[0].text = "Ce qu'on retient"
    t.text_frame.paragraphs[0].font.size = Pt(36)
    t.text_frame.paragraphs[0].font.bold = True
    t.text_frame.paragraphs[0].font.color.rgb = WHITE

    points = [
      "Infrastructure hybride réelle et démontrable à 90 %",
      "Sécurité : IPsec, double pfSense, bastion, Vault, Wazuh",
      "Tout est documenté, versionné et rejouable (IaC + DRP)",
      "Prochaines étapes : terraform apply, HTTPS, kill switch chrono",
    ]
    for i, pt in enumerate(points):
      y = 3.6 + i * 0.75
      dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.9), Inches(y), Inches(0.2), Inches(0.2))
      dot.fill.solid()
      dot.fill.fore_color.rgb = TEAL
      dot.line.fill.background()
      tx = s.shapes.add_textbox(Inches(1.3), Inches(y - 0.05), Inches(10), Inches(0.5))
      tx.text_frame.paragraphs[0].text = pt
      tx.text_frame.paragraphs[0].font.size = Pt(18)
      tx.text_frame.paragraphs[0].font.color.rgb = LIGHT_GRAY

    thanks = s.shapes.add_textbox(Inches(0.9), Inches(6.5), Inches(11), Inches(0.8))
    thanks.text_frame.paragraphs[0].text = "Merci — Questions ?"
    thanks.text_frame.paragraphs[0].font.size = Pt(28)
    thanks.text_frame.paragraphs[0].font.bold = True
    thanks.text_frame.paragraphs[0].font.color.rgb = GOLD
    thanks.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

  def build(self) -> Presentation:
    self.slide_cover()
    self.slide_agenda()
    self.slide_problem()
    self.slide_stats()
    self.slide_timeline()
    self.slide_team()
    self.slide_architecture()
    self.slide_site2_detail()
    self.slide_vpn()
    self.slide_firewall_bastion()
    self.slide_infraservice()
    self.slide_netbox_vault()
    self.slide_wazuh()
    self.slide_iac()
    self.slide_kill_drp()
    self.slide_git()
    self.slide_demo()
    self.slide_conclusion()
    return self.prs


def main() -> int:
  OUT_DIR.mkdir(parents=True, exist_ok=True)
  out = OUT_DIR / "CIA-Soutenance-T-NSA-810.pptx"

  prs = Deck().build()
  prs.save(str(out))
  prs.save(str(OUT_ROOT))

  print(f"✓ Présentation générée : {out}")
  print(f"✓ Copie racine         : {OUT_ROOT}")
  print(f"✓ Slides               : {len(prs.slides)}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
