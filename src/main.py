from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QStatusBar
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

    def _create_status_bar(self):
        status_bar = QStatusBar(self)
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
