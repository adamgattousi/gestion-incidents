import os
import sqlite3


def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    folder = os.path.dirname(db_path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    conn = get_connection(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT NOT NULL,
            lieu TEXT NOT NULL,
            priorite TEXT NOT NULL,
            statut TEXT NOT NULL DEFAULT 'Nouveau'
        )
    """)
    conn.commit()
    conn.close()


def get_all_incidents(db_path):
    conn = get_connection(db_path)
    incidents = conn.execute("SELECT * FROM incidents ORDER BY id DESC").fetchall()
    conn.close()
    return incidents


def add_incident(db_path, titre, description, lieu, priorite):
    conn = get_connection(db_path)
    conn.execute(
        "INSERT INTO incidents (titre, description, lieu, priorite) VALUES (?, ?, ?, ?)",
        (titre, description, lieu, priorite),
    )
    conn.commit()
    conn.close()
