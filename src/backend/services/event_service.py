import sqlite3


def get_all_events(db):
    cur = db.cursor()
    results = cur.execute("""
    SELECT * FROM events
    """).fetchall()
    return [dict(row) for row in results]
