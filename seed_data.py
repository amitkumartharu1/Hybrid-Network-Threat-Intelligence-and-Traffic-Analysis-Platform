"""
seed_data.py — Populate the database with realistic sample data for demo/testing.

Run:  python seed_data.py
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from datetime import datetime, timedelta
import random
import json
import uuid

from app import create_app, db
from app.models.packet import Packet
from app.models.flow import Flow
from app.models.alert import Alert
from app.models.ioc import IOC

app = create_app()

PROTOCOLS = ["TCP", "UDP", "ICMP", "DNS", "ARP"]
INTERNAL_IPS = ["192.168.1.10", "192.168.1.20", "192.168.1.50", "10.0.0.5", "10.0.0.12"]
EXTERNAL_IPS = [
    "185.220.101.12",   # known Tor exit node range
    "194.165.16.11",
    "45.33.32.156",     # nmap.org
    "8.8.8.8",
    "1.1.1.1",
    "23.96.34.100",
    "104.21.14.122",
]
COMMON_PORTS = [80, 443, 22, 53, 8080, 3389, 21, 25, 110, 143, 3306, 6379]


def seed():
    with app.app_context():
        # Don't re-seed if data already exists
        if Packet.query.count() > 0:
            print("Database already has data. Skipping seed.")
            return

        session_id = "demo-" + str(uuid.uuid4())[:8]
        now = datetime.utcnow()
        packets = []
        flows_data = {}

        print("Seeding packets and flows…")

        for i in range(500):
            src_ip = random.choice(INTERNAL_IPS + EXTERNAL_IPS)
            dst_ip = random.choice(INTERNAL_IPS + EXTERNAL_IPS)
            protocol = random.choice(PROTOCOLS)
            src_port = random.randint(1024, 65535)
            dst_port = random.choice(COMMON_PORTS)
            length = random.randint(40, 1500)
            ts = now - timedelta(seconds=random.randint(0, 3600))
            tcp_flags = random.choice(["S", "SA", "A", "FA", "R", None, None]) if protocol == "TCP" else None

            pkt = Packet(
                session_id=session_id,
                timestamp=ts,
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_port=src_port,
                dst_port=dst_port,
                protocol=protocol,
                length=length,
                tcp_flags=tcp_flags,
                payload_preview=None,
            )
            packets.append(pkt)

            # Group into flows
            key = (min(src_ip, dst_ip), max(src_ip, dst_ip), min(src_port, dst_port), max(src_port, dst_port), protocol)
            if key not in flows_data:
                flows_data[key] = {"pkts": [], "timestamps": []}
            flows_data[key]["pkts"].append(pkt)
            flows_data[key]["timestamps"].append(ts)

        db.session.add_all(packets)
        db.session.flush()

        flows = []
        for key, data in list(flows_data.items())[:80]:
            src_ip, dst_ip, src_port, dst_port, proto = key
            pkts = data["pkts"]
            ts_list = sorted(data["timestamps"])
            duration = (ts_list[-1] - ts_list[0]).total_seconds() if len(ts_list) > 1 else 0
            total_bytes = sum(random.randint(40, 1500) for _ in pkts)
            syn_c = sum(1 for p in pkts if p.tcp_flags and "S" in p.tcp_flags and "A" not in p.tcp_flags)
            ack_c = sum(1 for p in pkts if p.tcp_flags and "A" in p.tcp_flags)

            f = Flow(
                session_id=session_id,
                src_ip=src_ip, dst_ip=dst_ip,
                src_port=src_port, dst_port=dst_port,
                protocol=proto,
                start_time=ts_list[0], end_time=ts_list[-1],
                duration_seconds=duration,
                packet_count=len(pkts),
                total_bytes=total_bytes,
                avg_packet_size=total_bytes / len(pkts),
                syn_count=syn_c, ack_count=ack_c,
                fin_count=random.randint(0, 2),
                rst_count=random.randint(0, 3),
            )
            flows.append(f)

        db.session.add_all(flows)
        db.session.flush()

        for i, flow in enumerate(flows):
            for pkt in list(flows_data.values())[i]["pkts"]:
                pkt.flow_id = flow.id

        print("Seeding IOCs…")
        iocs = [
            IOC(indicator="185.220.101.12",  ioc_type="ip",      severity="Critical", description="Known Tor exit node", source="seed"),
            IOC(indicator="194.165.16.11",   ioc_type="ip",      severity="High",     description="C2 server",           source="seed"),
            IOC(indicator="evil-domain.com", ioc_type="domain",  severity="High",     description="Malware C2 domain",   source="seed"),
            IOC(indicator="malware",         ioc_type="keyword", severity="High",     description="Payload keyword",     source="seed"),
            IOC(indicator="4444",            ioc_type="port",    severity="Medium",   description="Metasploit default",  source="seed"),
        ]
        db.session.add_all(iocs)
        db.session.flush()

        print("Seeding alerts…")
        rules = ["port_scan", "syn_flood", "dns_tunneling", "ioc_ip_match", "isolation_forest_anomaly", "repeated_rst"]
        severities = ["Low", "Medium", "High", "Critical"]
        alert_list = []
        for i in range(20):
            rule = random.choice(rules)
            sev = random.choice(severities)
            score = {"Low": random.randint(5,24), "Medium": random.randint(25,49),
                     "High": random.randint(50,74), "Critical": random.randint(75,100)}[sev]
            src = random.choice(INTERNAL_IPS + EXTERNAL_IPS)
            dst = random.choice(EXTERNAL_IPS)
            det_type = "ioc" if "ioc" in rule else ("ml" if "forest" in rule else "rule")
            a = Alert(
                session_id=session_id,
                detection_type=det_type,
                rule_name=rule,
                flow_id=random.choice(flows).id if flows else None,
                src_ip=src, dst_ip=dst,
                dst_port=random.choice(COMMON_PORTS),
                risk_score=score, severity=sev,
                description=f"Seeded {rule} alert from {src}",
                evidence=json.dumps({"seed": True, "rule": rule}),
                score_breakdown=json.dumps({"rule_detection": score}),
                status=random.choice(["open", "open", "open", "reviewing", "closed"]),
                created_at=now - timedelta(minutes=random.randint(0, 120)),
            )
            alert_list.append(a)
        db.session.add_all(alert_list)
        db.session.commit()

        print(f"✓ Seeded: {len(packets)} packets, {len(flows)} flows, {len(iocs)} IOCs, {len(alert_list)} alerts.")
        print(f"  Session ID: {session_id}")
        print("  Login: admin / admin123")


if __name__ == "__main__":
    seed()
