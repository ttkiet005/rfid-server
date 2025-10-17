# import pandas as pd
# from datetime import datetime

# # --- ĐƯỜNG DẪN FILE ---
# path_students = r"C:\Users\ttkie\Desktop\test dakt\danhsachsinhvien.csv"
# path_schedule = r"C:\Users\ttkie\Desktop\test dakt\lichhoc.csv"
# path_output   = r"C:\Users\ttkie\Desktop\test dakt\diemdanh.csv"

# # --- 1. ĐỌC DỮ LIỆU ---
# students = pd.read_csv(path_students, dtype=str)
# schedule = pd.read_csv(path_schedule, dtype=str)

# print("✅ Đã đọc danh sách sinh viên và lịch học thành công.\n")

# # --- 2. HÀM MÔ PHỎNG QUÉT NFC ---
# def scan_nfc(uid):
#     """Kiểm tra UID thẻ NFC có trong danh sách sinh viên và lịch học hay không"""
#     now = datetime.now()
#     now_time = now.strftime("%H:%M:%S")
#     today = now.strftime("%Y-%m-%d")

#     # Tìm sinh viên có UID này
#     student = students.loc[students["UID"] == uid]

#     if student.empty:
#         print(f"❌ UID {uid} không có trong danh sách sinh viên.")
#         return None

#     student_id = student["StudentID"].values[0]
#     student_name = student["Name"].values[0]

#     # Tìm lịch học hôm nay
#     today_schedule = schedule.loc[schedule["Date"] == today]

#     if today_schedule.empty:
#         print(f"❌ Hôm nay ({today}) không có lịch học nào.")
#         return None

#     # Kiểm tra sinh viên có trong lịch học hôm nay không
#     match = today_schedule.loc[today_schedule["StudentID"] == student_id]

#     if not match.empty:
#         print(f"✅ Sinh viên {student_name} ({student_id}) có mặt lúc {now_time}")
#         record = {
#             "Subject": match["Subject"].values[0],
#             "Date": today,
#             "StartTime": match["StartTime"].values[0],
#             "EndTime": match["EndTime"].values[0],
#             "Room": match["Room"].values[0],
#             "StudentID": student_id,
#             "Name": student_name,
#             "UID": uid,
#             "Attendance": "Có mặt",
#             "TimeIn": now_time
#         }
#     else:
#         print(f"⚠️ Sinh viên {student_name} ({student_id}) KHÔNG có trong lịch học hôm nay.")
#         record = {
#             "Subject": "",
#             "Date": today,
#             "StartTime": "",
#             "EndTime": "",
#             "Room": "",
#             "StudentID": student_id,
#             "Name": student_name,
#             "UID": uid,
#             "Attendance": "Sai lịch học",
#             "TimeIn": now_time
#         }

#     return record


# # --- 3. DANH SÁCH MÃ UID GIẢ LẬP QUÉT ---
# # (sau này sẽ lấy từ module NFC thực tế)
# uids = [
#     "04A23BFF22",  # SV001
#     "037BC912DD",  # SV002
#     "FFFFFFFFFF",  # Không hợp lệ
#     "05BDE111AA",  # SV003
# ]

# records = []

# # --- 4. XỬ LÝ DANH SÁCH UID ---
# for uid in uids:
#     result = scan_nfc(uid)
#     if result:
#         records.append(result)

# # --- 5. GHI FILE ĐIỂM DANH ---
# if records:
#     attendance_df = pd.DataFrame(records)

#     # Đọc file diemdanh cũ nếu có, nối thêm dữ liệu mới
#     try:
#         old_df = pd.read_csv(path_output, dtype=str)
#         attendance_df = pd.concat([old_df, attendance_df], ignore_index=True)
#     except FileNotFoundError:
#         pass

#     attendance_df.to_csv(path_output, index=False, encoding="utf-8-sig")
#     print(f"\n💾 Đã lưu kết quả vào: {path_output}")
# else:
#     print("\n⚠️ Không có dữ liệu điểm danh nào được ghi.")

# # --- 6. TẠO DANH SÁCH ĐIỂM DANH CUỐI CÙNG (CÓ/VẮNG) ---
# today = datetime.now().strftime("%Y-%m-%d")
# today_schedule = schedule.loc[schedule["Date"] == today]

# final_list = today_schedule.merge(
#     students[["StudentID", "Name", "UID"]],
#     on="StudentID",
#     how="left"
# )

# # Đọc file điểm danh
# try:
#     attendance = pd.read_csv(path_output, dtype=str)
# except FileNotFoundError:
#     attendance = pd.DataFrame()

# final_list["Attendance"] = "Vắng"
# final_list["TimeIn"] = ""

# for i, row in final_list.iterrows():
#     matched = attendance[
#         (attendance["Date"] == today) &
#         (attendance["StudentID"] == row["StudentID"]) &
#         (attendance["Attendance"] == "Có mặt")
#     ]
#     if not matched.empty:
#         final_list.at[i, "Attendance"] = "Có mặt"
#         final_list.at[i, "TimeIn"] = matched["TimeIn"].values[-1]

# print("\n📋 DANH SÁCH ĐIỂM DANH HÔM NAY:")
# print(final_list)

# final_csv = fr"C:\Users\ttkie\Desktop\test dakt\diemdanh_{today}.csv"
# final_list.to_csv(final_csv, index=False, encoding="utf-8-sig")

# print(f"\n📤 Đã xuất file điểm danh cuối cùng: {final_csv}")
import gspread
from google.oauth2.service_account import Credentials

# ==== 1. Đường dẫn file JSON ====
SERVICE_ACCOUNT_FILE = r"C:\Users\ttkie\Desktop\test dakt\nfcdoor.json"

# ==== 2. Các quyền truy cập cần thiết ====
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# ==== 3. Kết nối Google Sheets ====
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# ==== 4. Mở file Google Sheet bằng ID ====
SPREADSHEET_ID = "1RBIXNP0O_EhoaIjoy-vsDkB6Jv_sy13NvsIy_UeVjas"  # file diemdanh
sheet = client.open_by_key(SPREADSHEET_ID).sheet1  # sheet đầu tiên trong file

# ==== 5. Ghi dữ liệu test ====
test_data = ["2025-10-14", "Nguyen Van A", "SV001", "Có mặt", "19:45"]
sheet.append_row(test_data)

print("✅ Đã ghi dữ liệu lên Google Sheet thành công!")
