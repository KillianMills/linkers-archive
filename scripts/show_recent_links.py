import sqlite3
import sys

DB_PATH = "data/links.db"

def main(limit=10):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "SELECT id, url, source, message_id, author, created_at FROM links ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
        if not rows:
            print("(no rows)")
            return
        for r in rows:
            print(r)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
    finally:
        try:
            conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    main()
