from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QStatusBar
from ui.cases.login_dialog import LoginDialog
import sys

from ui.cases.new_case_dialog import NewCaseDialog
from ui.cases.case_list_dialog import CaseListDialog
import os

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Forensic Case Management Tool")
        self.setGeometry(100, 100, 800, 600)
        self._create_menu_bar()
        self._create_status_bar()

    def _create_menu_bar(self):
        menubar = QMenuBar(self)
        file_menu = QMenu("File", self)
        help_menu = QMenu("Help", self)
        menubar.addMenu(file_menu)
        menubar.addMenu(help_menu)
        self.setMenuBar(menubar)

        # Add 'New Case' action
        new_case_action = file_menu.addAction("New Case")
        new_case_action.triggered.connect(self.open_new_case_dialog)

        # Add 'Open Case' action
        open_case_action = file_menu.addAction("Open Case")
        open_case_action.triggered.connect(self.open_case_list_dialog)

    def open_case_list_dialog(self):
        dialog = CaseListDialog(self.user_id)
        if dialog.exec_() == dialog.Accepted:
            case_path = dialog.selected_case_path
            # Read case metadata from the selected case DB
            try:
                import sqlite3
                conn = sqlite3.connect(case_path)
                cursor = conn.cursor()
                cursor.execute('SELECT case_name, investigator_name, description, date FROM CaseMetadata LIMIT 1')
                row = cursor.fetchone()
                conn.close()
                if row:
                    case_name, investigator, description, date = row
                    msg = f"Active Case: {case_name} | Investigator: {investigator} | Date: {date} | Description: {description}"
                    self.statusBar().showMessage(msg)
                else:
                    self.statusBar().showMessage(f"Opened case: {os.path.basename(case_path)} (metadata not found)")
            except Exception as e:
                self.statusBar().showMessage(f"Error loading case metadata: {str(e)}")

    def open_new_case_dialog(self):
        dialog = NewCaseDialog(self.user_id)
        if dialog.exec_() == dialog.Accepted:
            self.statusBar().showMessage("New case created successfully.")

    def _create_status_bar(self):
        status_bar = QStatusBar(self)
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    # Show login dialog first
    if login.exec_() == login.Accepted:
        window = MainWindow(login.user_id)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
