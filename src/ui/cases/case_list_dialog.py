from PyQt5.QtWidgets import QDialog, QLabel, QListWidget, QPushButton, QVBoxLayout, QMessageBox
import os
import sqlite3

CASES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../cases'))

class CaseListDialog(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Your Cases")
        self.setFixedSize(400, 300)
        self.selected_case_path = None
        self._setup_ui()
        self._load_cases()

    def _setup_ui(self):
        self.label = QLabel("Select a case to open:")
        self.list_widget = QListWidget()
        self.btn_open = QPushButton("Open Case")
        self.btn_open.clicked.connect(self.open_case)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.btn_open)
        self.setLayout(layout)

    def _load_cases(self):
        self.list_widget.clear()
        for fname in os.listdir(CASES_DIR):
            if fname.endswith('.db'):
                db_path = os.path.join(CASES_DIR, fname)
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT user_id, case_name, investigator_name, date FROM CaseMetadata LIMIT 1')
                    row = cursor.fetchone()
                    conn.close()
                    if row and row[0] == self.user_id:
                        display_text = f"{row[1]} (Investigator: {row[2]}, Date: {row[3]})"
                        self.list_widget.addItem(f"{display_text}||{db_path}")
                except Exception:
                    continue

    def open_case(self):
        selected = self.list_widget.currentItem()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a case to open.")
            return
        # Extract db_path from item text
        item_text = selected.text()
        if '||' in item_text:
            _, db_path = item_text.split('||', 1)
            self.selected_case_path = db_path
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid case selection.")
