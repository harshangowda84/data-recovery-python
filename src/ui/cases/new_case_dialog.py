from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QTextEdit, QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate
import sqlite3
import os

CASES_DIR = os.path.join(os.path.dirname(__file__), '../../cases')
if not os.path.exists(CASES_DIR):
    os.makedirs(CASES_DIR)

class NewCaseDialog(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Create New Case")
        self.setFixedSize(400, 320)
        self._setup_ui()

    def _setup_ui(self):
        self.label_case_name = QLabel("Case Name:")
        self.input_case_name = QLineEdit()
        self.label_investigator = QLabel("Investigator Name:")
        self.input_investigator = QLineEdit()
        self.label_description = QLabel("Description:")
        self.input_description = QTextEdit()
        self.label_date = QLabel("Date:")
        self.input_date = QDateEdit()
        self.input_date.setDate(QDate.currentDate())
        self.btn_create = QPushButton("Create Case")
        self.btn_create.clicked.connect(self.create_case)

        grid = QGridLayout()
        grid.addWidget(self.label_case_name, 0, 0)
        grid.addWidget(self.input_case_name, 0, 1)
        grid.addWidget(self.label_investigator, 1, 0)
        grid.addWidget(self.input_investigator, 1, 1)
        grid.addWidget(self.label_description, 2, 0)
        grid.addWidget(self.input_description, 2, 1)
        grid.addWidget(self.label_date, 3, 0)
        grid.addWidget(self.input_date, 3, 1)
        grid.addWidget(self.btn_create, 4, 0, 1, 2)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def create_case(self):
        case_name = self.input_case_name.text().strip()
        investigator = self.input_investigator.text().strip()
        description = self.input_description.toPlainText().strip()
        date = self.input_date.date().toString("yyyy-MM-dd")
        if not case_name or not investigator:
            QMessageBox.warning(self, "Input Error", "Case name and investigator are required.")
            return
        db_filename = f"case_{self.user_id}_{case_name.replace(' ', '_')}.db"
        db_path = os.path.join(CASES_DIR, db_filename)
        if os.path.exists(db_path):
            QMessageBox.warning(self, "Duplicate Case", "A case with this name already exists for this user.")
            return
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS CaseMetadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            case_name TEXT NOT NULL,
            investigator_name TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )''')
        cursor.execute('''INSERT INTO CaseMetadata (user_id, case_name, investigator_name, description, date)
                          VALUES (?, ?, ?, ?, ?)''',
                       (self.user_id, case_name, investigator, description, date))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Case created successfully.")
        self.accept()
