import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from .sheets_service import get_sheets_service, append_to_sheet
from .email_parser import parse_message

from config import STATE_FILE, SCOPES, TOKEN_FILE, CREDENTIALS_FILE, SPREADSHEET_ID

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_state(processed_ids):
    with open(STATE_FILE, "w") as f:
        json.dump(list(processed_ids), f)

# --- Main function ---
def main():
    # Authenticate APIs
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    # Load previously processed emails
    processed_ids = load_state()
    new_rows = []

    # Fetch unread emails
    messages = fetch_unread_emails(gmail)

    for msg in messages:
        msg_id = msg["id"]
        if msg_id in processed_ids:
            continue

        full_msg = gmail.users().messages().get(
            userId="me", id=msg_id, format="full"
        ).execute()

        MAX_CHARS = 50000  # Google Sheets max per cell
        row = parse_message(full_msg)

        # Truncate the email body (column D)
        sender, subject, date, body = row
        body = body[:MAX_CHARS]

        new_rows.append([sender, subject, date, body])

        mark_as_read(gmail, msg_id)
        processed_ids.add(msg_id)

    # Append new emails to Google Sheet
    if new_rows:
        append_to_sheet(sheets, new_rows)
        save_state(processed_ids)
        print(f"{len(new_rows)} emails added to Google Sheet.")
    else:
        print("No new unread emails found.")

# --- Entry point ---
if __name__ == "__main__":
    main()
