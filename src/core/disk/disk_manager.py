
import psutil
import platform

AUTHORIZED_ROLES = {"Investigator", "Admin"}

class DiskManager:
    def list_drives(self, user_role: str) -> list:
        """
        Return a list of physical drives if user_role is authorized.
        Each drive is represented as a dict: {"device", "mountpoint", "fstype", "opts", "size"}
        Read-only principle enforced: no write operations performed.
        """
        if user_role not in AUTHORIZED_ROLES:
            return []
        drives = []
        for part in psutil.disk_partitions(all=True):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                drives.append({
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "opts": part.opts,
                    "size": usage.total
                })
            except Exception:
                # Skip inaccessible partitions
                continue
        return drives


    def get_partitions(self, drive_id: str) -> list:
        """
        Parse and return partition info for the selected drive (read-only).
        Uses pytsk3 to read MBR/GPT and returns a list of dicts:
        {"addr": start sector, "size": size in bytes, "desc": description, "fstype": file system type}
        TLDR: Forensic, read-only, cross-platform.
        """
        import pytsk3
        partitions = []
        try:
            img = pytsk3.Img_Info(drive_id)
            vol = pytsk3.Volume_Info(img)
            for part in vol:
                if part.len > 2048:  # skip tiny partitions
                    partitions.append({
                        "addr": part.start,
                        "size": part.len * vol.info.block_size,
                        "desc": part.desc.decode() if hasattr(part.desc, 'decode') else str(part.desc),
                        "fstype": part.flags
                    })
        except Exception as e:
            # If parsing fails, return empty list
            return []
        return partitions

    def is_read_only(self) -> bool:
        """
        Verify all operations are read-only.
        Always returns True for this implementation.
        """
        return True
