
AUTHORIZED_ROLES = {"Investigator", "Admin"}

class DiskView:
    def show_drive_list(self, drives: list):
        """
        Display detected drives in a table or list (read-only).
        TLDR: Only shows info, no write actions.
        """
        for drive in drives:
            print(f"Device: {drive['device']} | Mount: {drive['mountpoint']} | FS: {drive['fstype']} | Size: {drive['size']}")

    def show_partitions(self, partitions: list):
        """
        Display partition details for a selected drive (read-only).
        TLDR: Only shows info, no write actions.
        """
        for part in partitions:
            print(f"Start: {part['addr']} | Size: {part['size']} | Desc: {part['desc']} | FS Type: {part['fstype']}")

    def restrict_access(self, user_role: str):
        """
        Enable/disable scan initiation based on user role.
        TLDR: Only authorized roles can scan; others view only.
        """
        if user_role in AUTHORIZED_ROLES:
            print("Scan enabled for role:", user_role)
            return True
        else:
            print("Scan disabled for role:", user_role)
            return False
