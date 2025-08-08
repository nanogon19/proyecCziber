import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ── Flask ────────────────────────────────────────────────────────────────
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")  # Úsalo si firmás cookies
    ENC_KEY = os.getenv("ENC_KEY", "enc-key")

    # ── Base de datos (Neon / Postgres) ─────────────────────────────────────
    # Forzamos el driver psycopg2 si te pasan 'postgres://' o 'postgresql://'
    _db_url = (os.getenv("DATABASE_URL") or "").strip()
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif _db_url.startswith("postgresql://") and "+psycopg2" not in _db_url:
        _db_url = _db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pool sano + SSL para Neon. Podés tunear con variables de entorno si querés.
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,                                # valida conexión antes de usarla
        "pool_recycle": int(os.getenv("SQL_POOL_RECYCLE", "300")),  # recicla cada 5 min
        "pool_size": int(os.getenv("SQL_POOL_SIZE", "5")),
        "max_overflow": int(os.getenv("SQL_MAX_OVERFLOW", "10")),
        "connect_args": {
            # redundante si ya está en la URL, pero seguro
            "sslmode": os.getenv("PG_SSLMODE", "require"),
            "channel_binding": os.getenv("PG_CHANNEL_BINDING", "require"),
            # keepalives ayudan con desconexiones del lado del servidor
            "keepalives": int(os.getenv("PG_KEEPALIVES", "1")),
            "keepalives_idle": int(os.getenv("PG_KEEPALIVES_IDLE", "30")),
            "keepalives_interval": int(os.getenv("PG_KEEPALIVES_INTERVAL", "10")),
            "keepalives_count": int(os.getenv("PG_KEEPALIVES_COUNT", "5")),
        },
    }

    # ── JWT (si lo usás) ────────────────────────────────────────────────────
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_EXPIRES_HOURS", "24"))
    )

    # ── QoL ─────────────────────────────────────────────────────────────────
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True
