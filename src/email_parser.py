import base64
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime, parseaddr
import re

def extract_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""

def decode(data):
    if not data:
        return ""
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

def clean_text(text):
    """
    Remove unwanted whitespace characters, zero-width spaces, & multiple blank lines
    """
    # Normalize unicode spaces & zero-width spaces
    text = re.sub(r'[\u200b\u200c\u00a0\u202f\u3000]', ' ', text)
    # Convert all types of newlines to \n
    text = re.sub(r'\r\n|\r', '\n', text)
    # Replace multiple spaces/tabs with single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Remove leading/trailing spaces for each line
    lines = [line.strip() for line in text.splitlines()]
    # Keep only non-empty lines
    lines = [line for line in lines if line]
    # Join lines with single newline
    return "\n".join(lines)

def html_to_clean_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Replace <br>, <p>, <div> with newlines
    for br in soup.find_all(["br", "p", "div"]):
        br.insert_before("\n")

    text = soup.get_text()
    return clean_text(text)

def get_email_body(payload):
    """
    Recursively extract the email body.
    Prefer text/plain. If only HTML is present, convert to clean plain text.
    """
    if payload.get("parts"):
        for part in payload["parts"]:
            body = get_email_body(part)
            if body:
                return body

    mime_type = payload.get("mimeType")
    data = payload.get("body", {}).get("data")
    if not data:
        return ""

    text = decode(data)

    if mime_type == "text/html":
        text = html_to_clean_text(text)
    else:
        text = clean_text(text)

    return text.strip()

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

    return sender_email, subject, date, body
