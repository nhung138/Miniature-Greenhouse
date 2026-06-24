from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import threading
from database import DB_NAME, init_db
from ai_consultant import get_ai_transition_analysis

# Khởi tạo DB
init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trạng thái hệ thống
state = {"last_mode": None, "system_report": "Hệ thống đang khởi động...", "ai_advice": "Đang chờ dữ liệu..."}

# Báo cáo tức thì (Hardcoded)
ADVICE_MESSAGES = {
    "R_DAY": "Hệ thống đã tự động đóng mái che do độ ẩm tăng cao. Đây là biện pháp bảo vệ cần thiết. Bạn có thể cân nhắc kiểm tra hệ thống thoát nước để tối ưu hóa trong những lần mưa tới.",
    "R_NIGHT": "Đã chuyển sang chế độ an toàn ban đêm và đóng mái che để ổn định nhiệt độ. Mọi chỉ số hiện tại vẫn nằm trong ngưỡng kiểm soát tốt.",
    "SUNNY": "Cường độ ánh sáng đạt mức tối ưu cho sự phát triển của cây. Hệ thống đang tận dụng tốt điều kiện tự nhiên. Đây là cơ hội tốt để ghi nhận tốc độ tăng trưởng của cây.",
    "CLOUDY": "Điều kiện ánh sáng đang ở mức trung bình. Nếu tình trạng này kéo dài, có thể chúng ta sẽ cần cân nhắc bổ sung đèn tăng trưởng để đảm bảo hiệu suất quang hợp.",
    "NIGHT": "Hệ thống đã ổn định ở chế độ ban đêm. Nhiệt độ và độ ẩm đang duy trì tốt. Đây là thời gian lý tưởng để cây nghỉ ngơi và hồi phục năng lượng."
}

def run_ai_analysis(old_mode, new_mode, temp, hum):
    analysis = get_ai_transition_analysis(old_mode, new_mode, temp, hum)
    state["ai_advice"] = analysis

# Route: Cập nhật trạng thái từ main.py (Đây là "cửa" cho hardware gửi dữ liệu)
@app.post("/update-state")
async def update_state(request: Request):
    data = await request.json()
    new_mode = data.get("mode")
    temp = data.get("temp")
    hum = data.get("hum")
    
    # 1. Cập nhật báo cáo tức thì
    state["system_report"] = ADVICE_MESSAGES.get(new_mode, "Hệ thống đang hoạt động ổn định.")
    
    # 2. Nếu mode thay đổi, kích hoạt AI
    if state["last_mode"] != new_mode and state["last_mode"] is not None:
        state["ai_advice"] = "Hệ thống đang phân tích thay đổi..."
        threading.Thread(target=run_ai_analysis, args=(state["last_mode"], new_mode, temp, hum)).start()
    
    state["last_mode"] = new_mode
    return {"status": "ok"}

@app.get("/status")
def get_status():
    return state

# @app.get("/data")
# def get_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * id, time, temperature, humidity, light, mode FROM sensor_logs ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "time": r[1], "temp": r[2], "hum": r[3], "light": r[4], "mode": r[5]} for r in rows]
    except Exception as e:
        return {"error": str(e)}

@app.get("/data")
def get_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # Viết tách rõ ràng: ORDER -> dấu cách -> BY -> dấu cách -> id
        cursor.execute("SELECT * FROM sensor_logs ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        
        return [{"id": r[0], "time": r[1], "temp": r[2], "hum": r[3], "light": r[4], "mode": r[5]} for r in rows]
    except Exception as e:
        return {"error": f"Lỗi Database: {str(e)}"}

@app.get("/advice")
def get_advice():
    # Legacy support
    return {"advice": state["ai_advice"]}
