import sqlite3
import os

def add_evidence_to_case(case_db_path, file_name, md5_hash):
    """
    Add evidence to the active case database.
    Args:
        case_db_path (str): Path to the case's .db file
        file_name (str): Name of the evidence file
        md5_hash (str): MD5 hash of the evidence file
    Returns:
        bool: True if successful, False otherwise
    """
    if not os.path.exists(case_db_path):
        return False
    try:
        conn = sqlite3.connect(case_db_path)
        cursor = conn.cursor()
        # Get case_id from CaseMetadata
        cursor.execute('SELECT id FROM CaseMetadata LIMIT 1')
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
        case_id = result[0]
        # Create Evidence table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS Evidence (
            evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            md5_hash TEXT,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(case_id) REFERENCES CaseMetadata(id)
        )''')
        # Insert evidence
        cursor.execute('''INSERT INTO Evidence (case_id, file_name, md5_hash) VALUES (?, ?, ?)''',
                       (case_id, file_name, md5_hash))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
