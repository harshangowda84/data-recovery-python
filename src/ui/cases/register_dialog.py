from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
import sqlite3
import hashlib
import os

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DB_DIR = os.path.join(WORKSPACE_ROOT, 'db')
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
USERS_DB = os.path.join(DB_DIR, 'users.db')

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register New Account")
        self.setFixedSize(360, 260)
        self._setup_ui()
        self._setup_db()

    def _setup_ui(self):
        title = QLabel("Create Your Account")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        self.label_user = QLabel("Username:")
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Choose a username")
        self.label_pass = QLabel("Password:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setPlaceholderText("Choose a password")
        self.label_confirm = QLabel("Confirm Password:")
        self.input_confirm = QLineEdit()
        self.input_confirm.setEchoMode(QLineEdit.Password)
        self.input_confirm.setPlaceholderText("Re-enter password")

        self.btn_register = QPushButton("Register")
        self.btn_register.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.btn_register.clicked.connect(self.handle_register)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: #c0392b; font-weight: bold;")

        grid = QGridLayout()
        grid.addWidget(self.label_user, 0, 0)
        grid.addWidget(self.input_user, 0, 1)
        grid.addWidget(self.label_pass, 1, 0)
        grid.addWidget(self.input_pass, 1, 1)
        grid.addWidget(self.label_confirm, 2, 0)
        grid.addWidget(self.input_confirm, 2, 1)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addWidget(self.message_label)
        main_layout.addWidget(self.btn_register)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(main_layout)

    def _setup_db(self):
        conn = sqlite3.connect(USERS_DB)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )''')
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def handle_register(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text()
        confirm = self.input_confirm.text()
        self.message_label.setText("")
        if not username or not password or not confirm:
            self.message_label.setText("All fields are required.")
            return
        if len(password) < 6:
            self.message_label.setText("Password must be at least 6 characters.")
            return
        if password != confirm:
            self.message_label.setText("Passwords do not match.")
            return
        try:
            conn = sqlite3.connect(USERS_DB)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                           (username, self.hash_password(password)))
            conn.commit()
            conn.close()
            self.message_label.setStyleSheet("color: #27ae60; font-weight: bold;")
            self.message_label.setText("Registration successful. You can now log in.")
            self.accept()
        except sqlite3.IntegrityError:
            self.message_label.setText("Username already exists.")
        except Exception as e:
            self.message_label.setText(f"Registration error: {str(e)}")
