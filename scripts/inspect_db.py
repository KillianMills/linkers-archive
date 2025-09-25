import sqlite3

DB = 'data/links.db'

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("PRAGMA table_info(links)")
print('schema:', cur.fetchall())
cur.execute("SELECT * FROM links LIMIT 5")
rows = cur.fetchall()
print('rows:', rows)
conn.close()
