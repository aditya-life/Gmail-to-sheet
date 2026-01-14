Gmail to Google Sheets Automation (Python)

**Author:** Aditya Kumar  
**Language:** Python 3  
**APIs Used:** Gmail API, Google Sheets API  
**Authentication:** OAuth 2.0


**Project Overview**

This project automates reading unread emails from Gmail and logs them into Google Sheets using Python. It uses Gmail API and Google Sheets API with OAuth 2.0 authentication. Each email is stored only once, and the system safely remembers previously processed emails.

*High-Level Architecture*

        ┌────────────┐
        │   Gmail    │
        │  (Inbox)   │
        └─────┬──────┘
              │ Gmail API
              ▼
     ┌──────────────────┐
     │  gmail_service.py│
     └─────────┬────────┘
               ▼
     ┌──────────────────┐
     │  email_parser.py │
     └─────────┬────────┘
               ▼
     ┌──────────────────┐
     │ sheets_service.py│ ───▶ Google Sheets
     └─────────┬────────┘
               ▼
           main.py
               │
               ▼
        state.json (last processed email)

*Project Structure*

    gmail-to-sheets/
    ├── src/
    │   ├── gmail_service.py
    │   ├── sheets_service.py
    │   ├── email_parser.py
    │   └── main.py
    ├── credentials/
    │   └── credentials.json
    ├── proof
    ├── config.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md

**Setup Instructions**

1. Clone repository

2. Install dependencies

3. Enable Gmail API & Google Sheets API

4. Configure OAuth consent screen

5. Create OAuth Client ID (Desktop App)

6. Download credentials.json into /credentials

7. Create Google Sheet and copy Spreadsheet ID

8. Run:

        python src/main.py


9. Browser will open → Login → Grant access → Emails sync to Sheets.

**OAuth Flow Used**

- This project uses OAuth 2.0 Installed App Flow.
The user authenticates via browser, grants access, and Google returns a secure access token which is stored locally and reused for future executions.

- This avoids storing passwords and allows the user to revoke access anytime.


**Duplicate Prevention Logic**

*Duplicates are prevented by:*

- Fetching only INBOX + UNREAD emails

- Storing processed Gmail message IDs in a local state file

- Marking emails as read after successful insertion

- If the script is run again, previously processed emails are skipped.

**State Persistence Method**

1. State is stored in a local file called:

        state.json


    Example:

        {
         "last_processed_email_id": "18c91abf29c..."
        }


**Why this approach:**

- Gmail IDs are unique and permanent

- Lightweight and fast

- Prevents reprocessing

- Survives script restarts

Execution Flow

- Authenticate user

- Fetch unread emails

- Parse sender, subject, date, body

- Append rows to Google Sheets

- Update state file

- Mark emails as read

**Challenge Faced & Solution**

- Challenge:
Gmail emails often arrive in complex MIME formats with nested parts and base64 encoding.

- Solution:
A recursive parser was implemented to safely extract and decode text/plain content, with fallback handling for HTML emails.

**Limitations**

- Works only with unread Inbox emails

- Gmail API quota limits apply

- Requires one-time manual OAuth login

- Not real-time (runs on execution)