import os
import google.generativeai as genai
import sqlite3
from dotenv import load_dotenv

# Nạp các biến môi trường từ file .env vào hệ thống ngầm
load_dotenv()      

# Lấy API Key một cách an toàn từ môi trường
api_key = os.getenv("GEMINI_API_KEY2")

# Cấu hình API Key bảo mật cho Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_ai_advice():
    conn = sqlite3.connect("greenhouse_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT temperature, humidity FROM sensor_logs ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    prompt = f"Dữ liệu 10 lần đo gần nhất (nhiệt độ, độ ẩm): {rows}. Hãy đưa ra lời khuyên ngắn (dưới 50 từ) chăm sóc cây."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI đang bận, thử lại sau nhé!"
# Trong ai_consultant.py
def generate_professional_advice(mode, temp, hum, light):
    persona = """
    Bạn là Chuyên gia Tư vấn Hệ thống Nông nghiệp Thông minh. 
    Phong cách: Lịch sự, chuyên nghiệp, khách quan và mang tính xây dựng.
    Bạn luôn coi chủ nhà là một đối tác kỹ thuật. Bạn không chỉ thông báo tình trạng, 
    mà còn phân tích dữ liệu để đề xuất các giải pháp tối ưu hóa năng suất.
    Mục tiêu: Giúp chủ nhà hiểu rõ hệ thống và đạt được kết quả tốt nhất.
    """
    
    # Logic phản ứng mang tính gợi ý phát triển
    events = {
        "R_DAY": "Hệ thống đã tự động đóng mái che do độ ẩm tăng cao. Đây là biện pháp bảo vệ cần thiết. Bạn có thể cân nhắc kiểm tra hệ thống thoát nước để tối ưu hóa trong những lần mưa tới.",
        "R_NIGHT": "Đã chuyển sang chế độ an toàn ban đêm và đóng mái che để ổn định nhiệt độ. Mọi chỉ số hiện tại vẫn nằm trong ngưỡng kiểm soát tốt.",
        "SUNNY": "Cường độ ánh sáng đạt mức tối ưu cho sự phát triển của cây. Hệ thống đang tận dụng tốt điều kiện tự nhiên. Đây là cơ hội tốt để ghi nhận tốc độ tăng trưởng của cây.",
        "CLOUDY": "Điều kiện ánh sáng đang ở mức trung bình. Nếu tình trạng này kéo dài, có thể chúng ta sẽ cần cân nhắc bổ sung đèn tăng trưởng để đảm bảo hiệu suất quang hợp.",
        "NIGHT": "Hệ thống đã ổn định ở chế độ ban đêm. Nhiệt độ và độ ẩm đang duy trì tốt. Đây là thời gian lý tưởng để cây nghỉ ngơi và hồi phục năng lượng."
    }
    
    base_text = events.get(mode, "Hệ thống đang hoạt động ổn định. Các thông số nằm trong ngưỡng cho phép.")
    
    prompt = f"""
    {persona}
    
    Thông tin hiện tại: 
    - Chế độ: {mode}
    - Nhiệt độ: {temp}°C
    - Độ ẩm: {hum}%
    - Ánh sáng: {light}
    
    Sự kiện: {base_text}
    
    Hãy viết một báo cáo ngắn gọn, lịch sự, bao gồm: 
    1. Trạng thái hiện tại.
    2. Một lời khuyên hoặc gợi ý kỹ thuật để hệ thống phát triển hơn trong tương lai.
    """
    
    response = model.generate_content(prompt)
    return response.text

ADVICE_MESSAGES = {
    "R_DAY": "Hệ thống đã tự động đóng mái che do độ ẩm tăng cao. Đây là biện pháp bảo vệ cần thiết. Bạn có thể cân nhắc kiểm tra hệ thống thoát nước để tối ưu hóa trong những lần mưa tới.",
    "R_NIGHT": "Đã chuyển sang chế độ an toàn ban đêm và đóng mái che để ổn định nhiệt độ. Mọi chỉ số hiện tại vẫn nằm trong ngưỡng kiểm soát tốt.",
    "SUNNY": "Cường độ ánh sáng đạt mức tối ưu cho sự phát triển của cây. Hệ thống đang tận dụng tốt điều kiện tự nhiên. Đây là cơ hội tốt để ghi nhận tốc độ tăng trưởng của cây.",
    "CLOUDY": "Điều kiện ánh sáng đang ở mức trung bình. Nếu tình trạng này kéo dài, có thể chúng ta sẽ cần cân nhắc bổ sung đèn tăng trưởng để đảm bảo hiệu suất quang hợp.",
    "NIGHT": "Hệ thống đã ổn định ở chế độ ban đêm. Nhiệt độ và độ ẩm đang duy trì tốt. Đây là thời gian lý tưởng để cây nghỉ ngơi và hồi phục năng lượng."
}

def get_pro_advice(mode):
    return ADVICE_MESSAGES.get(mode, "Hệ thống đang hoạt động ổn định. Các thông số nằm trong ngưỡng cho phép.")

def get_ai_transition_analysis(old_mode, new_mode, temp, hum):
    prompt = f"""
    Bạn là chuyên gia tư vấn nông nghiệp. 
    Hệ thống vừa chuyển trạng thái từ {old_mode} sang {new_mode}.
    Thông số: {temp}°C, {hum}% độ ẩm.
    
    Hãy phân tích:
    1. Tại sao sự chuyển đổi này là cần thiết?
    2. Cây trồng cần lưu ý gì ngay lúc này?
    Hãy trả lời ngắn gọn, chuyên nghiệp và mang tính xây dựng.
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    advice = get_ai_advice()
    with open("ai_advice.txt", "w", encoding="utf-8") as f:
        f.write(advice)