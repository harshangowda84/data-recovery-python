
import sys
import string
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QSizePolicy, QToolTip, QStyle,
    QTreeWidget, QTreeWidgetItem, QRadioButton, QButtonGroup, QLineEdit
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class DataReviverMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Reviver - Iterative data resurgance engine")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #f7f7fa;")
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left: Drive tree view
        drive_panel = QVBoxLayout()
        drive_label = QLabel("Drives")
        drive_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        drive_label.setStyleSheet("color: #2d3748; margin-bottom: 8px;")
        drive_panel.addWidget(drive_label)
        # Refresh Drives button at the top
        refresh_btn = QPushButton("⟳ Refresh Drives")
        refresh_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        refresh_btn.setStyleSheet("QPushButton {background-color: #42a5f5; color: white; border-radius: 8px; margin-bottom: 8px;} QPushButton:hover {background-color: #1976d2;}")
        refresh_btn.setCursor(Qt.PointingHandCursor)
        drive_panel.addWidget(refresh_btn)
        self.drive_tree = QTreeWidget()
        self.drive_tree.setHeaderHidden(True)
        self.drive_tree.setStyleSheet("background-color: #f7f7fa; border-radius: 8px;")
        # List drives
        drives = [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]
        for drv in drives:
            item = QTreeWidgetItem([drv])
            self.drive_tree.addTopLevelItem(item)
        self.drive_tree.setFixedWidth(220)
        drive_panel.addWidget(self.drive_tree)
        drive_panel.addStretch()
        main_layout.addLayout(drive_panel)

        # Right: Main area
        main_area = QVBoxLayout()
        main_layout.addLayout(main_area)

        # Blue scan header (clickable)
        self.scan_header = QFrame()
        self.scan_header.setStyleSheet("background-color: #2196f3; border-radius: 8px; margin-bottom: 12px;")
        self.scan_header.setCursor(Qt.PointingHandCursor)
        scan_header_layout = QHBoxLayout(self.scan_header)
        self.scan_title = QLabel("🔍 Start Scan")
        self.scan_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.scan_title.setStyleSheet("color: white;")
        scan_header_layout.addWidget(self.scan_title)
        scan_header_layout.addStretch()
        main_area.addWidget(self.scan_header)

        def scan_header_mousePressEvent(event):
            self.scan_drive()
        def scan_header_enterEvent(event):
            self.scan_header.setStyleSheet("background-color: #1976d2; border-radius: 8px; margin-bottom: 12px;")
            self.scan_title.setText("🚀 Start Advanced Scan")
        def scan_header_leaveEvent(event):
            self.scan_header.setStyleSheet("background-color: #2196f3; border-radius: 8px; margin-bottom: 12px;")
            self.scan_title.setText("🔍 Start Scan")
        self.scan_header.mousePressEvent = scan_header_mousePressEvent
        self.scan_header.enterEvent = scan_header_enterEvent
        self.scan_header.leaveEvent = scan_header_leaveEvent

        # Scan mode radio buttons (moved below scan header)
        scan_mode_layout = QHBoxLayout()
        self.scan_mode_group = QButtonGroup()
        self.basic_radio = QRadioButton("Basic Scan")
        self.basic_radio.setFont(QFont("Segoe UI", 11))
        self.basic_radio.setChecked(True)
        self.deep_radio = QRadioButton("Deep Scan")
        self.deep_radio.setFont(QFont("Segoe UI", 11))
        self.scan_mode_group.addButton(self.basic_radio)
        self.scan_mode_group.addButton(self.deep_radio)
        scan_mode_layout.addWidget(self.basic_radio)
        scan_mode_layout.addWidget(self.deep_radio)
        scan_mode_layout.addStretch()
        main_area.addLayout(scan_mode_layout)

        # Only one search bar above results table
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search files...")
        search_bar.setFont(QFont("Segoe UI", 11))
        search_bar.setStyleSheet("background-color: #e0e7ef; border-radius: 8px; padding: 8px; margin-bottom: 8px;")
        main_area.addWidget(search_bar)

        # Results Table
        self.results_table = QTableWidget(0, 6)
        self.results_table.setHorizontalHeaderLabels(["Name", "Type", "Size", "Last Modified", "Path", "Chance of Recovery"])
        self.results_table.setStyleSheet("background-color: #ffffff; border-radius: 8px; font-size: 11pt;")
        self.results_table.horizontalHeader().setStyleSheet("background-color: #e0e7ef; color: #2d3748; font-weight: bold;")
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setShowGrid(False)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.results_table.setColumnWidth(0, 180)
        self.results_table.setColumnWidth(1, 120)
        self.results_table.setColumnWidth(2, 100)
        self.results_table.setColumnWidth(3, 160)
        self.results_table.setColumnWidth(4, 220)
        self.results_table.setColumnWidth(5, 160)
        main_area.addWidget(self.results_table)

    # Only keep one restore button below the main results table

    def scan_drive(self):
        # Find the results table
        table = None
        main_layout = self.centralWidget().layout()
        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if isinstance(item, QVBoxLayout):
                for j in range(item.count()):
                    widget = item.itemAt(j).widget()
                    if isinstance(widget, QTableWidget):
                        table = widget
                        break
        if not table:
            print("Results table not found!")
            return

        import os
        import datetime
        # Get selected drive from drive tree
        selected_items = self.drive_tree.selectedItems()
        if not selected_items:
            # No drive selected
            results = [["Error: No drive selected. Please select a drive from the list.", "-", "-", "-", "-", "-"]]
        else:
            selected_drive = selected_items[0].text(0)
            results = []
            if self.basic_radio.isChecked():
                # Basic Scan: List files from Recycle Bin on selected drive (simulate)
                try:
                    recycle_bin = os.path.join(selected_drive, '$Recycle.Bin')
                    for root, dirs, files in os.walk(recycle_bin):
                        for file in files:
                            file_path = os.path.join(root, file)
                            try:
                                stat = os.stat(file_path)
                                size = stat.st_size
                                mtime = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%d-%m-%Y %H:%M:%S')
                                results.append([
                                    file,
                                    "Unknown",
                                    f"{size/1024:.2f} KB",
                                    mtime,
                                    file_path,
                                    "Unknown"
                                ])
                            except Exception:
                                continue
                    if not results:
                        results = [["No deleted files found in Recycle Bin", "-", "-", "-", "-", "-"]]
                except Exception as e:
                    results = [[f"Error: {str(e)}", "-", "-", "-", "-", "-"]]
            elif self.deep_radio.isChecked():
                # Deep Scan: Use pytsk3 to scan for deleted files on selected drive
                try:
                    import pytsk3
                    img = pytsk3.Img_Info(selected_drive)
                    fs = pytsk3.FS_Info(img)
                    for dir_entry in fs.open_dir(path="/"):
                        if not hasattr(dir_entry, "info") or not dir_entry.info.meta:
                            continue
                        meta = dir_entry.info.meta
                        if meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                            name = dir_entry.info.name.name.decode('utf-8', errors='ignore')
                            size = meta.size
                            mtime = meta.mtime
                            mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%d-%m-%Y %H:%M:%S') if mtime else "-"
                            results.append([
                                name,
                                "Unknown",
                                f"{size/1024:.2f} KB",
                                mtime_str,
                                selected_drive,
                                "Deleted"
                            ])
                    if not results:
                        results = [["No deleted files found (deep scan)", "-", "-", "-", "-", "-"]]
                except Exception as e:
                    results = [[f"Error: {str(e)}", "-", "-", "-", "-", "-"]]
                    meta = dir_entry.info.meta
                    if meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
                        name = dir_entry.info.name.name.decode('utf-8', errors='ignore')
                        size = meta.size
                        mtime = meta.mtime
                        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%d-%m-%Y %H:%M:%S') if mtime else "-"
                        results.append([
                            name,
                            "Unknown",
                            f"{size/1024:.2f} KB",
                            mtime_str,
                            selected_drive,
                            "Deleted"
                        ])
                    if not results:
                        results = [["No deleted files found (deep scan)", "-", "-", "-", "-", "-"]]
                except Exception as e:
                    results = [[f"Error: {str(e)}", "-", "-", "-", "-", "-"]]

        table.setRowCount(len(results))
        for row, data in enumerate(results):
            for col, value in enumerate(data):
                table.setItem(row, col, QTableWidgetItem(str(value)))
        print("Scan complete. Results updated.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataReviverMainWindow()
    window.show()
    sys.exit(app.exec_())
