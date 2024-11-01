import sqlite3


def create_table():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            asset_id TEXT,
            attribute_id TEXT,
            timestamp TEXT,
            value TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def insert_message(asset_id, attribute_id, timestamp, value):
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO messages (asset_id, attribute_id, timestamp, value)
        VALUES (?, ?, ?, ?)
    """,
        (asset_id, attribute_id, timestamp, value),
    )
    conn.commit()
    conn.close()
