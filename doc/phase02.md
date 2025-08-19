# Stage 2 Detailed Plan: Case Management Lifecycle 📂

## Goal
Implement the ability to create, open, and manage forensic cases within the application.

---

## Functional Requirements (FRs)

**FR1 - New Case Dialog:**  
The application shall provide a pop-up dialog window to enter metadata for a new case (Case ID, Investigator Name, Description, and Date).

**FR2 - Case Creation:**  
The application shall create a dedicated SQLite database file for each new case, stored in the `/cases` directory.

**FR3 - Load Case:**  
The application shall provide functionality to open an existing case file (`.db`) and load its data into the application.

**FR4 - Active Case Display:**  
The application shall display the active case’s metadata (Case ID, Investigator Name, Date, Description) in the main window once loaded.

**FR5 - Evidence Linkage:**  
The application shall ensure that all recovered files and metadata are linked to the currently active case in the database.

---

## Non-Functional Requirements (NFRs)

**NFR1 - Usability:**  
Case creation and loading workflows must be intuitive and require minimal user input.

**NFR2 - Maintainability:**  
Case-related functionality must be encapsulated in dedicated modules under `/core/cases` and `/db`.  
Dialogs and case UI components must reside under `/ui/cases`.

**NFR3 - Data Integrity:**  
Each case database file must be self-contained and protected from modification outside the application.

**NFR4 - Technology Stack:**  
SQLite will be used for per-case databases, accessed via Python’s built-in `sqlite3` library or an ORM.

---

## Desired Output for Stage 2

- A `new_case_dialog.py` (under `/ui/cases`) that allows input of case metadata.  
- A `case_manager.py` (under `/core/cases`) that handles creation, loading, and switching of case databases.  
- Generated `.db` files stored in `/cases` directory, one per case.  
- Active case details visible in the main window when a case is opened.  


---

# Phase 2 Development Plan (Reference)

This plan will be referred to at every step of development for Stage 2.

## Step 1: User Authentication & Registration
- Implement login and registration dialogs with clear UX and secure credential storage.
- Enforce that only authenticated users can access case management features.

## Step 2: Case Creation Workflow
- Build a new case dialog for entering case metadata.
- Link each case to the logged-in user's ID.
- On creation, generate a new SQLite DB for the case in `/cases`.

## Step 3: Case Listing & Loading
- Display a list of cases owned by the logged-in user.
- Allow users to open and manage only their cases.
- Load case metadata into the main window upon selection.

## Step 4: Active Case Display
- Show active case details (ID, Investigator, Date, Description) in the main window/status bar.

## Step 5: Evidence Linkage
- Ensure all recovered files and metadata are linked to the currently active case in its database.

## Step 6: Data Integrity & Security
- Validate user and case input.
- Restrict access to case files and databases at the application level.

## Step 7: Usability & Maintainability
- Keep workflows intuitive and minimize user input.
- Encapsulate case and user logic in dedicated modules.
- Document code and user flows for future maintenance.
