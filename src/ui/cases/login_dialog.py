from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from .register_dialog import RegisterDialog
from PyQt5.QtGui import QIcon, QFont
import sqlite3
import hashlib
import os

# Always resolve users.db relative to workspace root
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DB_DIR = os.path.join(WORKSPACE_ROOT, 'db')
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
USERS_DB = os.path.join(DB_DIR, 'users.db')

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Forensic Case Manager - Login")
        self.setFixedSize(360, 260)
        self.setWindowIcon(QIcon())  # Optionally set an icon here
        self.user_id = None
        self._setup_ui()
        self._setup_db()

    def _setup_ui(self):
        title = QLabel("Welcome to Forensic Case Manager")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")

        self.label_user = QLabel("Username:")
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Enter your username")
        self.label_pass = QLabel("Password:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        self.input_pass.setPlaceholderText("Enter your password")

        self.btn_login = QPushButton("Login")
        self.btn_login.setStyleSheet("background-color: #2980b9; color: white; font-weight: bold;")
        self.btn_register = QPushButton("Register")
        self.btn_register.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        self.btn_login.clicked.connect(self.handle_login)
        self.btn_register.clicked.connect(self.open_register_dialog)

        self.message_label = QLabel("")
        self.message_label.setStyleSheet("color: #c0392b; font-weight: bold;")

        grid = QGridLayout()
        grid.addWidget(self.label_user, 0, 0)
        grid.addWidget(self.input_user, 0, 1)
        grid.addWidget(self.label_pass, 1, 0)
        grid.addWidget(self.input_pass, 1, 1)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_register)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addWidget(self.message_label)
        main_layout.addLayout(btn_layout)
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

    def handle_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text()
        self.message_label.setText("")
        if not username or not password:
            self.message_label.setText("Please enter both username and password.")
            return
        if len(password) < 6:
            self.message_label.setText("Password must be at least 6 characters.")
            return
        try:
            conn = sqlite3.connect(USERS_DB)
            cursor = conn.cursor()
            cursor.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            conn.close()
            if result and self.hash_password(password) == result[1]:
                self.user_id = result[0]
                self.message_label.setStyleSheet("color: #27ae60; font-weight: bold;")
                self.message_label.setText(f"Welcome, {username}!")
                self.accept()
            else:
                self.message_label.setText("Invalid username or password.")
        except Exception as e:
            self.message_label.setText(f"Login error: {str(e)}")

    def open_register_dialog(self):
        dialog = RegisterDialog()
        if dialog.exec_() == dialog.Accepted:
            self.message_label.setStyleSheet("color: #27ae60; font-weight: bold;")
            self.message_label.setText("Registration successful. You can now log in.")
