import gspread
from google.oauth2.service_account import Credentials
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheets_client():
    """
    Authenticates with Google Sheets using a service account.
    Requires GOOGLE_SERVICE_ACCOUNT_JSON env var pointing to
    your service account credentials JSON file path.
    """
    creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_path:
        return None
    creds = Credentials.from_service_account_file(
        creds_path, scopes=SCOPES
    )
    return gspread.authorize(creds)


def sync_question_to_sheets(question):
    """
    Appends a new accepted question to Google Sheets.
    Called AFTER successful PostgreSQL insert.
    Fails silently so Sheets issues never block question saving.
    """
    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not spreadsheet_id:
        return

    try:
        client = get_sheets_client()
        if not client:
            return

        sheet = client.open_by_key(spreadsheet_id).sheet1

        row = [
            question.get("question_id", ""),
            question.get("question_type", ""),
            question.get("question_text", ""),
            question.get("instructions", ""),
            question.get("options", ""),
            question.get("correct_answer", ""),
            question.get("correct_answer_position", ""),
            question.get("explanation", ""),
            question.get("difficulty", ""),
            question.get("domain", ""),
            question.get("question_purpose", ""),
        ]
        sheet.append_row(row)

    except Exception as e:
        # Never block question saving due to Sheets issues
        print(f"[SHEETS SYNC WARNING] Could not sync to Sheets: {e}")
