import sqlite3
from pathlib import Path


DB_PATH = "db/nifty100.db"
SCHEMA_PATH = "db/schema.sql"


def create_database():

    Path("db").mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    with open(
        SCHEMA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        conn.executescript(
            file.read()
        )

    conn.commit()
    conn.close()

    print(
        "Database created successfully"
    )


if __name__ == "__main__":
    create_database()