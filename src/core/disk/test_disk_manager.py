from ..disk_manager import DiskManager
from ....ui.disk.disk_view import DiskView

# Test roles
roles = ["Investigator", "Admin", "Viewer"]
disk_manager = DiskManager()
disk_view = DiskView()

def test_drive_detection():
    for role in roles:
        drives = disk_manager.list_drives(role)
        print(f"Role: {role} - Drives detected: {len(drives)}")
        disk_view.show_drive_list(drives)
        can_scan = disk_view.restrict_access(role)
        print(f"Can scan: {can_scan}\n")
        if drives and can_scan:
            # Test partition parsing for first drive
            partitions = disk_manager.get_partitions(drives[0]['device'])
            print(f"Partitions for {drives[0]['device']}:")
            disk_view.show_partitions(partitions)
            print()

if __name__ == "__main__":
    test_drive_detection()
