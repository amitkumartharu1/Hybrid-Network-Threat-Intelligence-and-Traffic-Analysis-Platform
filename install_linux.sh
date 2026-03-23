#!/bin/bash
# ThreatWatch — Linux/macOS Setup Script

set -e

echo ""
echo "============================================"
echo " ThreatWatch Linux/macOS Installation"
echo "============================================"
echo ""

# Upgrade pip
echo "[1/4] Upgrading pip..."
pip install --upgrade pip -q

# Core packages
echo "[2/4] Installing core Flask stack..."
pip install Flask==3.0.3 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 \
    Flask-WTF==1.2.1 Werkzeug==3.0.3 SQLAlchemy==2.0.31 -q

# Data/ML
echo "[3/4] Installing data and ML packages..."
pip install pandas==2.1.4 scikit-learn==1.4.2 numpy==1.26.4 joblib==1.4.2 -q

# Utilities and capture
echo "[4/4] Installing remaining packages..."
pip install scapy==2.5.0 requests==2.32.3 fpdf2==2.7.9 python-dotenv==1.0.1 -q

# Optional
pip install python-whois -q 2>/dev/null && echo "  python-whois: installed" || echo "  python-whois: skipped (optional)"

echo ""
echo "============================================"
echo " Verifying installation..."
echo "============================================"
python3 -c "import flask; print('Flask:', flask.__version__)"
python3 -c "import flask_sqlalchemy; print('Flask-SQLAlchemy: OK')"
python3 -c "import flask_login; print('Flask-Login: OK')"
python3 -c "import pandas; print('pandas:', pandas.__version__)"
python3 -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
python3 -c "import scapy; print('Scapy: OK')"

echo ""
echo "All OK. Now run:"
echo "  python3 seed_data.py   # load demo data"
echo "  sudo python3 app.py    # sudo needed for packet capture"
echo ""
