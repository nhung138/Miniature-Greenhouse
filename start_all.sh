#!/bin/bash
PROJECT_DIR="/home/s1/Documents/Boongs/miniature_greenhouse"
PYTHON_VENV="$PROJECT_DIR/.venv/bin/python"

echo "Đang khởi động hệ thống..."

# 1. Chạy phần cứng: "Bơm" số 1 và số 0 vào để bỏ qua các câu hỏi input
cd "$PROJECT_DIR"
echo -e "1\n0" | sudo $PYTHON_VENV main.py > hardware.log 2>&1 &
echo "Đã khởi động: Phần cứng (main.py)"

# 2. Chạy Backend
cd "$PROJECT_DIR"
/usr/bin/python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
echo "Đã khởi động: API Backend"

# 3. Chạy Frontend
cd "$PROJECT_DIR/greenhouse-dashboard"
npm run dev > frontend.log 2>&1 &
echo "Đã khởi động: Web Dashboard"

echo "Hệ thống đã chạy xong hoàn toàn!"