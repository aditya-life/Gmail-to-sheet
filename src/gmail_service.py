import os
import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SCOPES, TOKEN_FILE, CREDENTIALS_FILE

def get_gmail_service():
    creds = None

    # Load token if exists
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, perform OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        os.makedirs("credentials", exist_ok=True)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def fetch_unread_emails(service):
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    return results.get("messages", [])

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()
