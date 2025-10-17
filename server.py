from flask import Flask, request
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

app = Flask(__name__)

# ======= Google Sheets =======
SERVICE_ACCOUNT_FILE = "nfcdoor.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)
SPREADSHEET_ID = "1RBIXNP0O_EhoaIjoy-vsDkB6Jv_sy13NvsIy_UeVjas"
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

@app.route("/rfid", methods=["POST"])
def rfid():
    data = request.json
    if not data:
        return {"status":"error","message":"No JSON received"}, 400

    uid = data.get("uid","")
    name = data.get("name","")
    studentId = data.get("studentId","")
    result = data.get("result","OK")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([timestamp, name, studentId, uid, result])
    return {"status":"ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=11000)
