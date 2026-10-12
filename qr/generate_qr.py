#!/usr/bin/env python3
"""Generate QR codes for URLs and WiFi networks.

Usage examples:
  python generate_qr.py url https://example.com --out example_url.png
  python generate_qr.py wifi --ssid MyNet --password secret --security WPA --out wifi.png
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import qrcode


def make_qr(data: str, out: Path, scale: int = 4) -> Path:
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((img.size[0] * scale, img.size[1] * scale))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def url_command(args: argparse.Namespace) -> int:
    out = Path(args.out) if args.out else Path("qr_url.png")
    path = make_qr(args.url, out)
    print(f"Saved URL QR to: {path}")
    return 0


def wifi_command(args: argparse.Namespace) -> int:
    # Format: WIFI:T:WPA;S:mynetwork;P:mypass;H:true;;
    security = args.security.upper() if args.security else "WPA"
    hidden = "true" if args.hidden else "false"
    # For open networks use nopass
    if security in ("NONE", "NOPASS", "OPEN"):
        payload = f"WIFI:T:nopass;S:{args.ssid};;"
    else:
        payload = f"WIFI:T:{security};S:{args.ssid};P:{args.password};H:{hidden};;"
    out = Path(args.out) if args.out else Path("qr_wifi.png")
    path = make_qr(payload, out)
    print(f"Saved WiFi QR to: {path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate QR codes for URLs and WiFi networks")
    sub = parser.add_subparsers(dest="cmd")

    p_url = sub.add_parser("url", help="Generate a QR code for a URL")
    p_url.add_argument("url", help="The URL to encode")
    p_url.add_argument("--out", help="Output filename (png)")
    p_url.set_defaults(func=url_command)

    p_wifi = sub.add_parser("wifi", help="Generate a QR code for WiFi credentials")
    p_wifi.add_argument("--ssid", required=True, help="WiFi SSID")
    p_wifi.add_argument("--password", default="", help="WiFi password (omit for open networks)")
    p_wifi.add_argument("--security", choices=["WPA","WEP","nopass","open","NONE"], default="WPA", help="Security type")
    p_wifi.add_argument("--hidden", action="store_true", help="Set hidden=true in payload")
    p_wifi.add_argument("--out", help="Output filename (png)")
    p_wifi.set_defaults(func=wifi_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    # If no arguments provided, offer interactive choice
    if len(argv) == 0:
        return interactive_flow()

    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


def interactive_flow() -> int:
    print("Kies wat je wilt genereren:")
    print("  1) URL QR-code")
    print("  2) WiFi QR-code")
    # Removed freeform JSON filename input. Instead list JSON files found
    # in this script's folder and let the user pick one, or enter manual.
    choice = input("Kies 1 of 2: ").strip()
    if choice == "1":
        # Look for JSON config files that contain a 'url' key
        cfg_dir = Path(__file__).parent
        candidates: list[Path] = []
        for p in sorted(cfg_dir.glob("*.json")):
            try:
                with p.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
            except Exception:
                continue
            if isinstance(data, dict) and "url" in data:
                candidates.append(p)

        if candidates:
            print("Gevonden URL-config bestanden:")
            print("  0) Handmatige invoer")
            for i, p in enumerate(candidates, start=1):
                print(f"  {i}) {p.name}")
            sel = input("Kies nummer (0 voor handmatig): ").strip()
            if sel == "0":
                url = input("URL: ").strip()
                if not url:
                    print("Geen URL opgegeven. Afgebroken.")
                    return 1
                out = input("Output filename (png) [qr_url.png]: ").strip() or "qr_url.png"
                make_qr(url, Path(out))
                print(f"Saved URL QR to: {out}")
                return 0
            try:
                idx = int(sel) - 1
                cfg_path = candidates[idx]
            except Exception:
                print("Ongeldige selectie.")
                return 1
            try:
                with cfg_path.open("r", encoding="utf-8") as fh:
                    conf = json.load(fh)
            except Exception as e:
                print(f"Kon config niet lezen: {e}")
                return 1
            url = conf.get("url")
            out = conf.get("out", "qr_url.png")
            if not url:
                print("Gevonden config bevat geen 'url'.")
                return 1
            make_qr(url, Path(out))
            print(f"Saved URL QR to: {out}")
            return 0

        # No candidate configs found -> manual fallback
        url = input("URL: ").strip()
        if not url:
            print("Geen URL opgegeven. Afgebroken.")
            return 1
        out = input("Output filename (png) [qr_url.png]: ").strip() or "qr_url.png"
        make_qr(url, Path(out))
        print(f"Saved URL QR to: {out}")
        return 0
    if choice == "2":
        # Look for JSON config files that contain a 'ssid' key
        cfg_dir = Path(__file__).parent
        candidates: list[Path] = []
        for p in sorted(cfg_dir.glob("*.json")):
            try:
                with p.open("r", encoding="utf-8") as fh:
                    data = json.load(fh)
            except Exception:
                continue
            if isinstance(data, dict) and "ssid" in data:
                candidates.append(p)

        if candidates:
            print("Gevonden WiFi-config bestanden:")
            print("  0) Handmatige invoer")
            for i, p in enumerate(candidates, start=1):
                print(f"  {i}) {p.name}")
            sel = input("Kies nummer (0 voor handmatig): ").strip()
            if sel == "0":
                ssid = input("SSID: ").strip()
                if not ssid:
                    print("Geen SSID opgegeven. Afgebroken.")
                    return 1
                password = input("Password (leave empty for open): ")
                security = input("Security [WPA/WEP/nopass] (default WPA): ").strip() or "WPA"
                hidden_in = input("Hidden? (y/N): ").strip().lower()
                hidden = hidden_in == "y"
                if security.upper() in ("NONE", "NOPASS", "OPEN") or security.lower() in ("nopass", "open") or password == "":
                    payload = f"WIFI:T:nopass;S:{ssid};;"
                else:
                    payload = f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hidden else 'false'};;"
                out = input("Output filename (png) [qr_wifi.png]: ").strip() or "qr_wifi.png"
                make_qr(payload, Path(out))
                print(f"Saved WiFi QR to: {out}")
                return 0
            try:
                idx = int(sel) - 1
                cfg_path = candidates[idx]
            except Exception:
                print("Ongeldige selectie.")
                return 1
            try:
                with cfg_path.open("r", encoding="utf-8") as fh:
                    conf = json.load(fh)
            except Exception as e:
                print(f"Kon config niet lezen: {e}")
                return 1
            ssid = conf.get("ssid")
            if not ssid:
                print("Gevonden config bevat geen 'ssid'.")
                return 1
            password = conf.get("password", "")
            security = conf.get("security", "WPA")
            hidden = bool(conf.get("hidden", False))
            if security.upper() in ("NONE", "NOPASS", "OPEN") or security.lower() in ("nopass", "open") or not password:
                payload = f"WIFI:T:nopass;S:{ssid};;"
            else:
                payload = f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hidden else 'false'};;"
            out = conf.get("out", "qr_wifi.png")
            make_qr(payload, Path(out))
            print(f"Saved WiFi QR to: {out}")
            return 0

        # No candidate configs found -> manual fallback
        ssid = input("SSID: ").strip()
        if not ssid:
            print("Geen SSID opgegeven. Afgebroken.")
            return 1
        password = input("Password (leave empty for open): ")
        security = input("Security [WPA/WEP/nopass] (default WPA): ").strip() or "WPA"
        hidden_in = input("Hidden? (y/N): ").strip().lower()
        hidden = hidden_in == "y"
        if security.upper() in ("NONE", "NOPASS", "OPEN") or security.lower() in ("nopass", "open") or password == "":
            payload = f"WIFI:T:nopass;S:{ssid};;"
        else:
            payload = f"WIFI:T:{security};S:{ssid};P:{password};H:{'true' if hidden else 'false'};;"
        out = input("Output filename (png) [qr_wifi.png]: ").strip() or "qr_wifi.png"
        make_qr(payload, Path(out))
        print(f"Saved WiFi QR to: {out}")
        return 0

    print("Ongeldige keuze. Gebruik 1 of 2.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
