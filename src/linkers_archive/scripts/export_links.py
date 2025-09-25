import sqlite3
import csv
import json
import os
from pathlib import Path

DB_PATH = Path("data/links.db")

def export_csv(output="links.csv"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT url, first_seen, source, message_id, author FROM links ORDER BY first_seen")
    rows = cur.fetchall()
    conn.close()

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "first_seen", "source", "message_id", "author"])
        writer.writerows(rows)

    print(f"✅ Exported {len(rows)} links to {output}")

def export_json(output="links.json"):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT url, first_seen, source, message_id, author FROM links ORDER BY first_seen")
    rows = cur.fetchall()
    conn.close()

    data = [
        {
            "url": url,
            "first_seen": first_seen,
            "source": source,
            "message_id": message_id,
            "author": author,
        }
        for (url, first_seen, source, message_id, author) in rows
    ]

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {len(data)} links to {output}")

if __name__ == "__main__":
    os.makedirs("exports", exist_ok=True)
    export_csv("exports/links.csv")
    export_json("exports/links.json")
