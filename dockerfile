# 1. Chọn image Python cơ bản
FROM python:3.11-slim

# 2. Thiết lập thư mục làm việc trong container
WORKDIR /app

# 3. Copy file requirements và cài đặt thư viện
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy toàn bộ project vào container
COPY . .

# 5. Lệnh chạy Flask khi container khởi động
CMD ["python", "server.py"]
