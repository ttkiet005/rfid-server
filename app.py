from flask import Flask, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os

app = Flask(__name__)

# ======= Google Sheets =======
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# --- Load credentials ---
# Nếu chạy local: đọc file nfcdoor.json
# Nếu deploy Render: đọc từ biến môi trường SERVICE_ACCOUNT_JSON
if os.path.exists("nfcdoor.json"):
    with open("nfcdoor.json") as f:
        service_account_info = json.load(f)
else:
    service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
    if not service_account_json:
        raise Exception("❌ Missing Google credentials. Set SERVICE_ACCOUNT_JSON env var.")
    service_account_info = json.loads(service_account_json)

creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(creds)
SPREADSHEET_ID = "1RBIXNP0O_EhoaIjoy-vsDkB6Jv_sy13NvsIy_UeVjas"
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


@app.route("/rfid", methods=["POST"])
def rfid():
    data = request.json
    if not data:
        return {"status": "error", "message": "No JSON received"}, 400

    uid = data.get("uid", "")
    name = data.get("name", "")
    studentId = data.get("studentId", "")
    result = data.get("result", "OK")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([timestamp, name, studentId, uid, result])
    return {"status": "ok"}


@app.route("/", methods=["GET"])
def home():
    return "RFID server is running ✅"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=11000)
