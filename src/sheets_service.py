from googleapiclient.discovery import build
from .gmail_service import get_gmail_service
from config import SPREADSHEET_ID, SHEET_NAME

def get_sheets_service():
    # Reuse Gmail credentials for Sheets API
    creds = get_gmail_service()._http.credentials
    return build("sheets", "v4", credentials=creds)

def append_to_sheet(service, values):
    body = {"values": values}

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:D",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
