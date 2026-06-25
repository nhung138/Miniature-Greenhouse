from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import threading
from database import DB_NAME, init_db
#from ai_consultant import get_ai_transition_analysis
from ai_consultant import get_pro_advice

# Khởi tạo Cơ sở dữ liệu
init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Trạng thái hệ thống
state = {
    "last_mode": None, 
    "system_report": "Hệ thống đang khởi động...", 
    "ai_advice": "データを待機しています..."
}

# Báo cáo tức thì cho từng chế độ (Hardcoded)
# Báo cáo tức thì cho từng chế độ bằng tiếng Nhật (ADVICE_MESSAGES)
ADVICE_MESSAGES = {
    "R_DAY": "雨が降ってきたので、自動で屋根を閉じました！☔ 植物たちは安全だよ！✨",
    "R_NIGHT": "雨の夜モードです！🌙🌧️ 温度を守るために屋根を閉じました。すべて順調だよ！✨",
    "SUNNY": "ピカピカの晴れです！☀️ お日さまの光がたっぷりで、植物たちも大喜びだよ！🚀",
    "CLOUDY": "今は曇り空です☁️ お日さまは隠れているけど、みんな元気だよ！🌱",
    "NIGHT": "静かな夜モードです！🌙 温湿度もばっちりで、植物たちのおやすみタイムだよ💤"
}

# Định nghĩa các cặp chuyển đổi trạng thái được phép kích hoạt Gemini gọi AI
VALID_AI_TRANSITIONS = [
    ("SUNNY", "CLOUDY"),    # Từ SUNNY ➔ CLOUDY
    ("SUNNY", "R_DAY"),     # Từ SUNNY ➔ R_DAY
    ("R_DAY", "SUNNY"),     # Từ R_DAY ➔ SUNNY
    ("CLOUDY", "R_DAY"),    # Từ CLOUDY ➔ R_DAY
    ("CLOUDY", "SUNNY"),    # Từ CLOUDY ➔ SUNNY
    ("NIGHT", "R_NIGHT"),   # Từ NIGHT ➔ R_NIGHT
    ("R_NIGHT", "NIGHT")    # Từ R_NIGHT ➔ NIGHT
]

# def run_ai_analysis(old_mode, new_mode, temp, hum):
#     try:
#         analysis = get_ai_transition_analysis(old_mode, new_mode, temp, hum)
#         state["ai_advice"] = analysis
#     except Exception as e:
#         err_msg = str(e)
#         # Bắt lỗi 429 Quota để hiển thị câu thông báo ngắn gọn theo yêu cầu
#         if "ResourceExhausted" in err_msg or "429" in err_msg or "Quota exceeded" in err_msg:
#             state["ai_advice"] = "本日の利用上限に達しました。" # Đã hết lượt sử dụng trong ngày.
#         else:
#             state["ai_advice"] = f"AI分析エラー：: {err_msg}"
            
#         print(f"[AI Error] Không thể lấy phân tích từ Gemini: {e}")

# def run_ai_analysis(old_mode, new_mode, temp, hum):
#     try:
#         # Gọi hàm mới (giả lập) thay vì gọi hàm cũ bị lỗi
#         analysis = get_pro_advice(new_mode) 
#         state["ai_advice"] = analysis
#     except Exception as e:
#         state["ai_advice"] = f"AI Error: {str(e)}"
#         print(f"[AI Error] Lỗi hệ thống: {e}")
# def run_ai_analysis(old_mode, new_mode, temp, hum):
#     # Chỉ gọi đúng hàm giả lập và lấy kết quả trả về
#     analysis = get_pro_advice(new_mode, previous_mode=old_mode, temp=temp, hum=hum)
#     state["ai_advice"] = analysis

def run_ai_analysis(old_mode, new_mode, temp, hum):
    try:
        # TRUYỀN THÊM old_mode VÀO ĐÂY
        analysis = get_pro_advice(new_mode, previous_mode=old_mode)
        state["ai_advice"] = analysis
    except Exception as e:
        state["ai_advice"] = "AI分析エラー"
        print(f"[AI Error] Lỗi: {e}")

# Route: Cập nhật trạng thái từ main.py (Hardware gửi dữ liệu lên đây)
#@app.post("/update-state")
# async def update_state(request: Request):
#     data = await request.json()
#     new_mode = data.get("mode")
#     temp = data.get("temp")
#     hum = data.get("hum")
    
#     old_mode = state["last_mode"]
    
#     # Trong file api.py, đoạn route update-state:
#     analysis = get_pro_advice(new_mode, previous_mode=old_mode) # Phải truyền old_mode vào
#     state["ai_advice"] = analysis

#     # 1. Cập nhật báo cáo tĩnh tức thì trên giao diện
#     state["system_report"] = ADVICE_MESSAGES.get(new_mode, "システムは安定して稼働しています。") #Hệ thống đang hoạt động ổn định.
    
#     # 2. Kiểm tra bộ lọc điều kiện để kích hoạt AI (Chặn dội bom Quota 429)
#     if old_mode is not None and old_mode != new_mode:
#         # if (old_mode, new_mode) in VALID_AI_TRANSITIONS:
#         #     print(f"[AI Trigger] Chuyển đổi hợp lệ: {old_mode} ➔ {new_mode}. Đang gọi Gemini...")
#         #     state["ai_advice"] = "Hệ thống đang phân tích thay đổi..."
#         #     threading.Thread(target=run_ai_analysis, args=(old_mode, new_mode, temp, hum)).start()
#         # else:
#         #     print(f"[AI Skip] Chuyển đổi: {old_mode} ➔ {new_mode}. Không cần gọi AI, bỏ qua để tiết kiệm Quota.")
#         if (old_mode, new_mode) in VALID_AI_TRANSITIONS:
#             print(f"[AI Trigger] Chuyển đổi hợp lệ: {old_mode} ➔ {new_mode}. Đang gọi AI Giả lập...")
#             # state["ai_advice"] = get_pro_advice(new_mode, previous_mode=old_mode)
#             state["ai_advice"] = "Hệ thống đang phân tích..."
#             state["ai_advice"] = get_pro_advice(new_mode, previous_mode=old_mode)
#             # Gọi hàm trực tiếp hoặc qua thread
#             # state["ai_advice"] = get_pro_advice(new_mode) 
#         else:
#             print(f"[AI Skip] Chuyển đổi: {old_mode} ➔ {new_mode}. Bỏ qua.") 
#     state["last_mode"] = new_mode
#     return {"status": "ok"}

@app.post("/update-state")
async def update_state(request: Request):
    data = await request.json()
    new_mode = data.get("mode")
    
    # Lấy old_mode từ state hiện tại
    old_mode = state["last_mode"]
    
    print(f"[DEBUG] Trạng thái: Old={old_mode} | New={new_mode}") # CẦN DÒNG NÀY ĐỂ CHECK LOG

    # Cập nhật lời khuyên AI - TRUYỀN ĐỦ THAM SỐ
    # Nếu old_mode là None (lần đầu tiên), ta lấy luôn current_mode làm previous cho nó đỡ báo lỗi
    prev = old_mode if old_mode is not None else new_mode
    state["system_report"] = ADVICE_MESSAGES.get(new_mode, f"システム稼働中: {new_mode}")
    # GỌI HÀM MỚI Ở ĐÂY
    state["ai_advice"] = get_pro_advice(new_mode, previous_mode=prev)
            
    # Cập nhật trạng thái cũ để lần sau dùng
    state["last_mode"] = new_mode 
    return {"status": "ok"}

# Route: Lấy trạng thái hiện tại hiển thị lên Dashboard
@app.get("/status")
def get_status():
    return state

# Route: Lấy dữ liệu lịch sử log cảm biến từ SQLite
@app.get("/data")
def get_data():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sensor_logs ORDER BY id DESC LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        
        return [{"id": r[0], "time": r[1], "temp": r[2], "hum": r[3], "light": r[4], "mode": r[5]} for r in rows]
    except Exception as e:
        return {"error": f"Lỗi Database: {str(e)}"}

# Route bổ trợ: Hỗ trợ các phân hệ cũ lấy lời khuyên AI
@app.get("/advice")
def get_advice():
    return {"advice": state["ai_advice"]}



if __name__ == "__main__":
    import uvicorn
    # Chỉ cần host và port, tuyệt đối không để reload=True
    uvicorn.run(app, host="0.0.0.0", port=8000)