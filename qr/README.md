# QR-code generator

Korte tool om QR-codes te genereren voor URL's en WiFi-netwerken.

Installatie

```powershell
python -m pip install -r qr/requirements.txt
```

Gebruik

URL:

```powershell
python qr/generate_qr.py url https://example.com --out example_url.png
```

WiFi:

```powershell
python qr/generate_qr.py wifi --ssid MijnNet --password geheim --security WPA --out wifi.png
```

Voorbeeldconfiguraties

- `example.url.json`: voorbeeld voor URL-generatie
- `example.wifi.json`: voorbeeld voor WiFi-generatie
