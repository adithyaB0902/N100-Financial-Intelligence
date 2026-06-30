import sqlite3
import os

# Project paths
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DB_FOLDER = os.path.join(PROJECT_ROOT, "db")
DB_PATH = os.path.join(DB_FOLDER, "nifty100.db")
SCHEMA_PATH = os.path.join(DB_FOLDER, "schema.sql")


def create_database():
    """
    Create SQLite database from schema.sql
    """

    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn.executescript(schema)

    conn.commit()
    conn.close()

    print("=" * 40)
    print("DATABASE CREATED SUCCESSFULLY")
    print("=" * 40)
    print(f"Database : {DB_PATH}")
    print(f"Schema   : {SCHEMA_PATH}")


if __name__ == "__main__":
    create_database()