import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_key_check;")
print("FK Check:")
print(cursor.fetchall())

print("\nCompanies Table Structure:")
cursor.execute("PRAGMA table_info(companies);")

for row in cursor.fetchall():
    print(row)

conn.close()