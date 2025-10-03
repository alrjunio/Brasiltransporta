import os, time, sys
import psycopg2

def _normalize(url: str) -> str:
    # Alembic/SQLAlchemy usam "postgresql+psycopg2://", mas psycopg2.connect espera "postgresql://"
    return url.replace("postgresql+psycopg2://", "postgresql://", 1)

def main() -> int:
    raw = os.getenv("DATABASE_URL")
    if not raw:
        print("DATABASE_URL não definido.", file=sys.stderr)
        return 1

    dsn = _normalize(raw)
    deadline = time.time() + 60  # até 60s de espera
    last_err = None

    while time.time() < deadline:
        try:
            conn = psycopg2.connect(dsn)
            conn.close()
            print("DB ok.")
            return 0
        except Exception as e:
            last_err = e
            print(f"Aguardando DB... {e}")
            time.sleep(2)

    print(f"Timeout ao conectar no DB: {last_err}", file=sys.stderr)
    return 1

if __name__ == "__main__":
    sys.exit(main())
