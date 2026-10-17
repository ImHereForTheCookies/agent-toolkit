"""Tiny sqlite3 data layer for the pantry API (stdlib only)."""
import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    quantity   INTEGER NOT NULL,
    unit       TEXT    NOT NULL,
    updated_at TEXT    NOT NULL
)
"""


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(db_path):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    conn = connect(db_path)
    try:
        with conn:
            conn.execute(SCHEMA)
    finally:
        conn.close()


def seed(db_path):
    """Insert a few starter items if the table is empty."""
    init_db(db_path)
    conn = connect(db_path)
    try:
        with conn:
            if conn.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0:
                for name, qty, unit in [("rice", 2, "kg"), ("olive oil", 1, "l"), ("eggs", 12, "pcs")]:
                    conn.execute(
                        "INSERT INTO items (name, quantity, unit, updated_at) VALUES (?, ?, ?, ?)",
                        (name, qty, unit, _now()),
                    )
    finally:
        conn.close()


def create_item(db_path, name, quantity, unit):
    conn = connect(db_path)
    try:
        with conn:
            cur = conn.execute(
                "INSERT INTO items (name, quantity, unit, updated_at) VALUES (?, ?, ?, ?)",
                (name, quantity, unit, _now()),
            )
            new_id = cur.lastrowid
        return get_item(db_path, new_id)
    finally:
        conn.close()


def list_items(db_path):
    conn = connect(db_path)
    try:
        rows = conn.execute("SELECT * FROM items ORDER BY id").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_item(db_path, item_id):
    conn = connect(db_path)
    try:
        row = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_item(db_path, item_id, fields):
    """Apply a dict of column -> value; returns the updated item or None if missing."""
    if get_item(db_path, item_id) is None:
        return None
    fields = dict(fields, updated_at=_now())
    assignments = ", ".join(f"{col} = ?" for col in fields)
    conn = connect(db_path)
    try:
        with conn:
            conn.execute(
                f"UPDATE items SET {assignments} WHERE id = ?",
                (*fields.values(), item_id),
            )
    finally:
        conn.close()
    return get_item(db_path, item_id)


def delete_item(db_path, item_id):
    conn = connect(db_path)
    try:
        with conn:
            cur = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
            return cur.rowcount > 0
    finally:
        conn.close()
