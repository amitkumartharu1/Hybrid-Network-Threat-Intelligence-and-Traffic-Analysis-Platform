"""
ThreatWatch — Hybrid Network Threat Intelligence Platform
Entry point. Run with:  python app.py
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,   # reloader interferes with Scapy background threads
    )
