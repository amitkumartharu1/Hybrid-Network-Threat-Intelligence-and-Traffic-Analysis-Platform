"""
ThreatWatch — Hybrid Network Threat Intelligence Platform
Entry point.

Run with:
    python run.py                # development
    sudo python run.py           # Linux/macOS (needed for Scapy raw socket)

On Windows run as Administrator, or use:
    python run.py
"""

import sys
import os

# Make sure the project root is on sys.path before anything else
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

application = create_app()   # WSGI-compatible name for production servers

if __name__ == "__main__":
    application.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,  # reloader conflicts with Scapy background threads
    )
