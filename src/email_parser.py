import base64
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime, parseaddr

def extract_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""

def get_email_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                return decode(part["body"].get("data"))
            if part["mimeType"] == "text/html":
                html = decode(part["body"].get("data"))
                return BeautifulSoup(html, "html.parser").get_text()
    return decode(payload["body"].get("data"))

def decode(data):
    if not data:
        return ""
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

def parse_message(message):
    headers = message["payload"]["headers"]

    sender_full = extract_header(headers, "From")
    sender_email = parseaddr(sender_full)[1]
    subject = extract_header(headers, "Subject")
    date_raw = extract_header(headers, "Date")

    try:
        date = parsedate_to_datetime(date_raw).strftime("%Y-%m-%d %H:%M:%S")
    except:
        date = date_raw

    body = get_email_body(message["payload"])

    return sender_email, subject, date, body.strip()
