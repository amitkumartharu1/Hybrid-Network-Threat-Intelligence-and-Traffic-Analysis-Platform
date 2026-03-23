# ThreatWatch — Hybrid Network Threat Intelligence Platform

A mini-SOC platform that captures live traffic, builds conversation flows,
detects threats via rule-based, IOC, and ML methods, scores risk, and
presents everything in a professional dark security dashboard.

---

## Quick Start

### Step 1 — Create a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2 — Install dependencies

**Windows (run the helper script):**
```bat
install_windows.bat
```

Or manually:
```bat
pip install --upgrade pip
pip install numpy==1.26.4
pip install pandas==2.1.4
pip install Flask==3.0.3 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Werkzeug==3.0.3 SQLAlchemy==2.0.31
pip install scikit-learn==1.4.2 joblib==1.4.2
pip install scapy==2.5.0 requests==2.32.3 fpdf2==2.7.9 python-dotenv==1.0.1
```

**Linux / macOS:**
```bash
bash install_linux.sh
```

### Step 3 — Configure environment

```bash
copy .env.example .env      # Windows
cp .env.example .env        # Linux/macOS
```

Edit `.env` — at minimum set your network interface:
```
CAPTURE_INTERFACE=eth0      # Linux
CAPTURE_INTERFACE=Wi-Fi     # Windows (use name from ipconfig)
SECRET_KEY=change-this-to-something-random
```

### Step 4 — Seed demo data (optional but recommended)

```bash
python seed_data.py
```

This creates 500 packets, 80 flows, 20 alerts, and 5 IOCs so the
dashboard is populated immediately.

### Step 5 — Run the app

```bash
# Windows (run as Administrator for Scapy capture)
python run.py

# Linux / macOS
sudo python3 run.py
```

Open: **http://localhost:5000**
Login: **admin / admin123**

> ⚠ Change the default password immediately via My Profile (⚙ icon in sidebar).

---

## Windows-Specific Notes

### Packet Capture
Scapy on Windows requires **Npcap** for raw socket access.
Download and install from: **https://npcap.com/**
Run Python / the app as **Administrator**.

### Finding your interface name
```bat
ipconfig
```
Common names: `Wi-Fi`, `Ethernet`, `Local Area Connection`

Set in `.env`:
```
CAPTURE_INTERFACE=Wi-Fi
```

### pandas installation error
If `pandas==2.2.2` fails (Meson/C compiler error), use:
```bat
pip install pandas==2.1.4
```
Version 2.1.4 has prebuilt Windows wheels and requires no compiler.

---

## Typical Workflow

```
1. Login              → Dashboard overview
2. Capture page       → Select interface → Start Capture
3. Capture page       → Stop Capture
4. Capture page       → Click "Build Flows"
5. Alerts page        → Click "Run Detection"
6. ML page            → Click "Train Model" (needs ≥20 flows)
7. Alerts page        → Run Detection again (now includes ML scores)
8. Investigation page → Click any alert for full evidence view
9. Reports page       → Download PDF / CSV report
```

## Detection Capabilities

| Rule | Trigger | Severity |
|------|---------|---------|
| Port Scan | ≥15 distinct dst ports from one source IP | High |
| SYN Flood | ≥200 SYNs with SYN/ACK ratio ≥5 | Critical |
| ARP Spoofing | ≥3 source IPs claiming same target IP | High |
| DNS Tunneling | DNS flow avg packet size >200B or >50 packets | High |
| Outbound Spike | Single flow >10× session average bytes | High |
| Repeated RST | Source IP with >30 RST packets | Medium |
| IOC Match | IP, domain, keyword, or port matches loaded IOC list | High/Critical |
| ML Anomaly | IsolationForest flags flow as outlier | Medium |

---

## Risk Score Logic

| Signal | Points |
|--------|--------|
| Rule hit (Critical) | +40 |
| Rule hit (High) | +30 |
| Rule hit (Medium) | +20 |
| IOC match | +40 |
| IOC Critical boost | +15 |
| ML anomaly | +0–25 |
| Bad reputation (VirusTotal) | +25 |

**Severity bands:** 0–24 Low · 25–49 Medium · 50–74 High · 75–100 Critical

---

## Advanced Features

| Feature | Access |
|---------|--------|
| Network Graph | Advanced → Network Graph |
| DPI Scanner | Advanced → DPI Scanner |
| Nmap Scanner | Advanced → Nmap Scanner (internal IPs only) |
| Session Reconstruction | Investigation → alert → Reconstruct Session |
| Baseline Comparison | Advanced → Baseline Compare |

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/capture/start` | Start packet capture |
| POST | `/capture/stop` | Stop packet capture |
| GET | `/capture/status` | Capture running state |
| POST | `/flows/build` | Aggregate packets into flows |
| POST | `/alerts/run-detection` | Run full detection pipeline |
| GET | `/dashboard/api/summary-stats` | Live stat counts |
| GET | `/dashboard/api/traffic-timeline` | Packets/min last hour |
| GET | `/advanced/api/graph-data` | Network graph JSON |
| POST | `/advanced/api/dpi-scan` | DPI scan a session |
| POST | `/advanced/api/nmap-scan` | Nmap scan a host |
| GET | `/health` | Health check (no auth) |

---

## Optional Integrations

**VirusTotal** — Set `VIRUSTOTAL_API_KEY` in `.env`.
Triggered manually per-alert via the "Enrich" button in the investigation view.
Free tier: 4 requests/minute.

**WHOIS** — Install `python-whois`:
```bash
pip install python-whois
```

**Nmap** —
- Windows: https://nmap.org/download.html
- Linux: `sudo apt install nmap`
- macOS: `brew install nmap`

---

## Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |

Change immediately via the ⚙ icon in the sidebar → My Profile.

---

## License

MIT — for educational and authorised security research use only.
Do not capture traffic on networks you do not own or have explicit written permission to test.
