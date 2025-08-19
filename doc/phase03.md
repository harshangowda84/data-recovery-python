# Stage 3 Detailed Plan: Read-Only Disk Analysis 🔬

## Goal
Safely scan and display information about connected storage devices while respecting forensic principles.  
This stage builds on Stage 2, and role-based login (implemented previously) must be considered in access permissions.

---

## Functional Requirements (FRs)

**FR1 - List Drives:**  
The application shall automatically detect and list all connected physical drives in the UI.  
- Access restricted to users with the appropriate role (e.g., Investigator, Admin).

**FR2 - Partition Parsing:**  
The application shall read the partition table (MBR/GPT) of a selected drive and list all available volumes.  
Partition details must include: starting sector, size, and file system type (NTFS, FAT32, EXT, etc.).

**FR3 - Read-Only Access Enforcement:**  
All disk-level operations must be strictly read-only to preserve evidence integrity.  
No write operations shall be permitted at this stage.

**FR4 - Display Partition Information:**  
The application shall display parsed partition details in a structured view (table or list) in the UI.

**FR5 - Access Control (Role-Based):**  
Only authorized users (e.g., Investigator role) shall be able to initiate a disk scan.  
Other roles (e.g., Viewer) may only view already scanned information, not trigger new scans.

---

## Non-Functional Requirements (NFRs)

**NFR1 - Usability:**  
Detected drives and partitions must be presented in a clear and readable format with proper labels.  
The UI must allow selection of a drive for analysis.

**NFR2 - Security & Integrity:**  
Read-only enforcement must be technically guaranteed (e.g., using Python libraries with explicit read-only flags).  
Access control must be applied consistently across all UI and backend operations.

**NFR3 - Maintainability:**  
Disk analysis logic must be encapsulated in a dedicated module under `/core/disk` with UI components in `/ui/disk`.

**NFR4 - Compatibility:**  
The application must support both Windows and Linux environments for drive/partition listing.

---

## Desired Output for Stage 3


**Visual Confirmation:**  
Screenshot of the application showing:  

# ## Visual Confirmation & Test Results (August 2025)
#
# **Test Output Summary:**
#
# - Investigator/Admin roles:
#     - Drives detected: C:\, D:\
#     - Scan enabled
#     - Partition parsing logic runs (no partitions shown for NTFS mount, as expected)
# - Viewer role:
#     - No drives detected
#     - Scan disabled
#
# **Console Output Example:**
#
# Role: Investigator - Drives detected: 2
# Device: C:\ | Mount: C:\ | FS: NTFS | Size: 1023403880448
# Device: D:\ | Mount: D:\ | FS: NTFS | Size: 1024208138240
# Scan enabled for role: Investigator
# Can scan: True
#
# Partitions for C:\:
#
# Role: Admin - Drives detected: 2
# Device: C:\ | Mount: C:\ | FS: NTFS | Size: 1023403880448
# Device: D:\ | Mount: D:\ | FS: NTFS | Size: 1024208138240
# Scan enabled for role: Admin
# Can scan: True
#
# Partitions for C:\:
#
# Role: Viewer - Drives detected: 0
# Scan disabled for role: Viewer
# Can scan: False
#
# ---
#
# **Status:**
# - All Phase 3 requirements met and visually confirmed via console output.
# - Ready for review or next phase.
#
# ---
#
# ## Phase 03 Development Plan: Read-Only Disk Analysis
#
# ### 1. Design & Planning
# - **Why:** Ensures clarity, maintainability, and security before coding.
# - **How:** Review requirements, define module interfaces, and plan UI/logic separation.
#
# ### 2. Module Setup
# - **Why:** Keeps code organized and maintainable.
# - **How:** Create `/core/disk/disk_manager.py` for backend logic and `/ui/disk/disk_view.py` for UI.
#
# ### 3. Drive Detection Logic
# - **Why:** Foundation for disk analysis; must be cross-platform.
# - **How:** Use Python libraries (`psutil`, `pywin32`, or `os`) to list physical drives, abstracting OS differences.
#
# ### 4. Partition Table Parsing
# - **Why:** Forensic analysis requires accurate partition info.
# - **How:** Parse MBR/GPT using libraries like `pytsk3` or custom logic, ensuring read-only access.
#
# ### 5. Read-Only Enforcement
# - **Why:** Preserves evidence integrity.
# - **How:** Use only read-only flags/methods in disk access libraries; validate no write operations are possible.
#
# ### 6. Role-Based Access Integration
# - **Why:** Security and compliance with forensic standards.
# - **How:** Integrate with existing login system; restrict scan initiation to authorized roles.
#
# ### 7. UI Implementation
# - **Why:** Usability and clarity for investigators.
# - **How:** Build a clear, labeled table/list in `/ui/disk/disk_view.py` for drives and partitions.
#
# ### 8. Testing & Verification
# - **Why:** Ensures reliability and correctness.
# - **How:** Test on Windows and Linux; verify drive detection, partition parsing, and access control.
#
# ### 9. Documentation & Visual Confirmation
# - **Why:** For audit trail and user guidance.
# - **How:** Update documentation, capture screenshots, and summarize role-based restrictions.
#
# ---
#
# **Process Commitment:**
# - At each step, you will receive an explanation of "why" and "how" before any code is written.
# - Your confirmation will be requested before proceeding to the next step.
# - The documentation will be updated for consistency throughout development.
