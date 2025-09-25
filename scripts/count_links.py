import sqlite3

def main():
    try:
        conn = sqlite3.connect("data/links.db")
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM links")
        n = cur.fetchone()[0]
        print(n)
    except Exception as e:
        print("ERROR:", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    main()
