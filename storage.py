import json
import sqlite3

DB_NAME = "runs.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            api TEXT NOT NULL,
            passed INTEGER NOT NULL,
            failed INTEGER NOT NULL,
            error_rate REAL NOT NULL,
            latency_ms_avg REAL NOT NULL,
            latency_ms_p95 REAL NOT NULL,
            availability TEXT NOT NULL,
            payload TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_run(run_data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO runs (
            timestamp, api, passed, failed, error_rate,
            latency_ms_avg, latency_ms_p95, availability, payload
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_data["timestamp"],
        run_data["api"],
        run_data["summary"]["passed"],
        run_data["summary"]["failed"],
        run_data["summary"]["error_rate"],
        run_data["summary"]["latency_ms_avg"],
        run_data["summary"]["latency_ms_p95"],
        run_data["summary"]["availability"],
        json.dumps(run_data)
    ))

    conn.commit()
    conn.close()


def list_runs(limit=20):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM runs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_last_run():
    runs = list_runs(limit=1)
    return runs[0] if runs else None