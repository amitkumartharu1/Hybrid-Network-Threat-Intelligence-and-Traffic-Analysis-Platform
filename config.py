import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "595573ac71c14b72deb28b3b83243f87b018b1262920ed5f9f574c82608ac41b")
    DEBUG = False
    TESTING = False

    # SQLite database stored in /instance
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "instance", "platform.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Packet capture
    DEFAULT_INTERFACE = os.getenv("CAPTURE_INTERFACE", "eth0")
    MAX_PACKETS_PER_CAPTURE = int(os.getenv("MAX_PACKETS", "10000"))
    PACKET_STORE_PAYLOAD_PREVIEW = True
    PAYLOAD_PREVIEW_LENGTH = 64  # bytes

    # Flow builder
    FLOW_TIMEOUT_SECONDS = 120  # flows idle for this long are finalized

    # Detection thresholds
    PORT_SCAN_THRESHOLD = 15       # distinct ports from one IP in a short window
    SYN_FLOOD_THRESHOLD = 200      # SYN packets per second
    DNS_PAYLOAD_THRESHOLD = 100    # bytes — unusually large DNS payload
    OUTBOUND_SPIKE_MULTIPLIER = 3  # x times the baseline before alerting

    # Risk scoring weights
    SCORE_IOC_MATCH = 40
    SCORE_RULE_HIT = 20
    SCORE_BAD_REPUTATION = 25
    SCORE_ML_ANOMALY = 15

    # Severity bands
    SEVERITY_LOW_MAX = 24
    SEVERITY_MEDIUM_MAX = 49
    SEVERITY_HIGH_MAX = 74
    # 75+ is Critical

    # ML
    MODEL_PATH = os.path.join(BASE_DIR, "app", "ml", "saved_models")
    ANOMALY_CONTAMINATION = 0.05  # expected fraction of anomalies for IsolationForest

    # Threat intelligence
    VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY", "b8b14536aed769b823fe93fecde054e821ab0ee7a385628ee5061db6ee871208")
    VIRUSTOTAL_ENABLED = bool(VIRUSTOTAL_API_KEY)
    GEOIP_DB_PATH = os.path.join(BASE_DIR, "datasets", "GeoLite2-City.mmdb")

    # Reports
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")

    # IOC dataset
    IOC_UPLOAD_DIR = os.path.join(BASE_DIR, "datasets", "ioc")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Choose which config to use via env var APP_ENV
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

active_config = config_map.get(os.getenv("APP_ENV", "development"), DevelopmentConfig)
