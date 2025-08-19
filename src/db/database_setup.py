import sqlite3

DB_NAME = 'forensic_cases.db'

CREATE_CASES_TABLE = '''
CREATE TABLE IF NOT EXISTS Cases (
    case_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investigator_name TEXT NOT NULL,
    case_name TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_EVIDENCE_TABLE = '''
CREATE TABLE IF NOT EXISTS Evidence (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    md5_hash TEXT,
    added_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(case_id) REFERENCES Cases(case_id)
);
'''

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_CASES_TABLE)
    cursor.execute(CREATE_EVIDENCE_TABLE)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database and tables created.")
