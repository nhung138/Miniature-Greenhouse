# import os
# import google.generativeai as genai
# import sqlite3
# from dotenv import load_dotenv

# # Nạp các biến môi trường từ file .env vào hệ thống ngầm
# load_dotenv()      

# # Lấy API Key một cách an toàn từ môi trường
# api_key = os.getenv("GEMINI_API_KEY2")

# # Cấu hình API Key bảo mật cho Gemini
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel('gemini-2.0-flash')

# def get_ai_advice():
#     conn = sqlite3.connect("greenhouse_data.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT temperature, humidity FROM sensor_logs ORDER BY id DESC LIMIT 10")
#     rows = cursor.fetchall()
#     conn.close()
    
#     prompt = f"Dữ liệu 10 lần đo gần nhất (nhiệt độ, độ ẩm): {rows}. Hãy đưa ra lời khuyên ngắn (dưới 50 từ) chăm sóc cây."
    
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except:
#         return "AI đang bận, thử lại sau nhé!"
# # Trong ai_consultant.py
# def generate_professional_advice(mode, temp, hum, light):
#     persona = """
#     Bạn là Chuyên gia Tư vấn Hệ thống Nông nghiệp Thông minh. 
#     Phong cách: Lịch sự, chuyên nghiệp, khách quan và mang tính xây dựng.
#     Bạn luôn coi chủ nhà là một đối tác kỹ thuật. Bạn không chỉ thông báo tình trạng, 
#     mà còn phân tích dữ liệu để đề xuất các giải pháp tối ưu hóa năng suất.
#     Mục tiêu: Giúp chủ nhà hiểu rõ hệ thống và đạt được kết quả tốt nhất.
#     """
    
#     # Logic phản ứng mang tính gợi ý phát triển
#     events = {
#         "R_DAY": "雨が降ってきたので、自動で屋根を閉じました！☔ 植物たちは安全だよ！✨",
#         "R_NIGHT": "雨の夜モードです！🌙🌧️ 温度を守るために屋根を閉じました。すべて順調だよ！✨",
#         "SUNNY": "ピカピカの晴れです！☀️ お日さまの光がたっぷりで、植物たちも大喜びだよ！🚀",
#         "CLOUDY": "今は曇り空です☁️ お日さまは隠れているけど、みんな元気だよ！🌱",
#         "NIGHT": "静かな夜モードです！🌙 温湿度もばっちりで、植物たちのおやすみタイムだよ💤"
#     }
    
#     base_text = events.get(mode, "Hệ thống đang hoạt động ổn định. Các thông số nằm trong ngưỡng cho phép.")
    
#     prompt = f"""
#     {persona}
    
#     Thông tin hiện tại: 
#     - Chế độ: {mode}
#     - Nhiệt độ: {temp}°C
#     - Độ ẩm: {hum}%
#     - Ánh sáng: {light}
    
#     Sự kiện: {base_text}
    
#     Hãy viết một báo cáo ngắn gọn, lịch sự, bao gồm: 
#     1. Trạng thái hiện tại.
#     2. Một lời khuyên hoặc gợi ý kỹ thuật để hệ thống phát triển hơn trong tương lai.
#     🚀 LƯU Ý CỰC KỲ QUAN TRỌNG CHO PHẦN HIỂN THỊ:
#     1. Phía trên: Hãy viết toàn bộ nội dung phân tích và lời khuyên bằng TIẾNG NHẬT (Japanese).
#     2. Phía dưới: Hãy dịch toàn bộ nội dung tiếng Nhật đó sang TIẾNG VIỆT (Vietnamese) một cách mượt mà.
#     3. Giọng điệu (Tone): Hãy dùng những từ ngữ thật vui tươi, năng động, tràn đầy năng lượng và truyền cảm hứng mạnh mẽ trong CẢ HAI NGÔN NGỮ nhé! Let's goooo! 🔥✨
#     """
    
#     response = model.generate_content(prompt)
#     return response.text

# # Đoạn tin nhắn tiếng Nhật ngắn gọn, đáng yêu và chung chung hơn
# ADVICE_MESSAGES = {
#     "R_DAY": "雨が降ってきたので、自動で屋根を閉じました！☔ 植物たちは安全だよ！✨",
#     "R_NIGHT": "雨の夜モードです！🌙🌧️ 温度を守るために屋根を閉じました。すべて順調だよ！✨",
#     "SUNNY": "ピカピカの晴れです！☀️ お日さまの光がたっぷりで、植物たちも大喜びだよ！🚀",
#     "CLOUDY": "今は曇り空です☁️ お日さまは隠れているけど、みんな元気だよ！🌱",
#     "NIGHT": "静かな夜モードです！🌙 温湿度もばっちりで、植物たちのおやすみタイムだよ💤"
# }

# def get_pro_advice(mode):
#     return ADVICE_MESSAGES.get(mode, "Hệ thống đang hoạt động ổn định. Các thông số nằm trong ngưỡng cho phép.")

# def get_ai_transition_analysis(mode, temp, hum, light):
#     prompt = f"""
#     Thông tin hiện tại: 
#     - Chế độ: {mode}
#     - Nhiệt độ: {temp}°C
#     - Độ ẩm: {hum}%
#     - Ánh sáng: {light}
    
    
#     Hãy viết một báo cáo ngắn gọn, lịch sự, bao gồm: 
#     1. Trạng thái hiện tại.
#     2. Một lời khuyên hoặc gợi ý kỹ thuật để hệ thống phát triển hơn trong tương lai.
#     🚀 LƯU Ý CỰC KỲ QUAN TRỌNG CHO PHẦN HIỂN THỊ:
#     1. Phía trên: Hãy viết toàn bộ nội dung phân tích và lời khuyên bằng TIẾNG NHẬT (Japanese).
#     2. Phía dưới: Hãy dịch toàn bộ nội dung tiếng Nhật đó sang TIẾNG VIỆT (Vietnamese) một cách mượt mà.
#     3. Giọng điệu (Tone): Hãy dùng những từ ngữ thật vui tươi, năng động, tràn đầy năng lượng và truyền cảm hứng mạnh mẽ trong CẢ HAI NGÔN NGỮ nhé! Let's goooo! 🔥✨
#     """
#     response = model.generate_content(prompt)
#     return response.text

# if __name__ == "__main__":
#     advice = get_ai_advice()
#     with open("ai_advice.txt", "w", encoding="utf-8") as f:
#         f.write(advice)

# import time
# import os
# from datetime import datetime, time as datetime_time
# # Giữ nguyên phần import google.generativeai của bạn ở đây...

# CACHE_FILE = "ai_advice_cache.txt"
# TIME_FILE = "last_ai_time.txt"
# COOLDOWN_SECONDS = 120  # Khóa cứng 2 phút chống spam tuyệt đối

# # def is_presentation_time():
# #     now = datetime.now()
# #     current_time = now.time()
# #     # Chấp nhận cả ngày 24, 25, 26 để đề phòng đồng hồ của Raspberry Pi bị lệch ngày!
# #     if now.year == 2026 and now.month == 6 and now.day in [24, 25, 26]:
# #         # Khung giờ 1: 10h - 11h sáng
# #         if datetime_time(10, 0) <= current_time <= datetime_time(11, 0):
# #             return True
# #         # Khung giờ 2: 12h30 - 17h chiều
# #         if datetime_time(12, 30) <= current_time <= datetime_time(17, 0):
# #             return True
# #     return False

# # def get_pro_advice(current_mode):
# #     # 1. Nếu ngoài giờ thuyết trình -> Khóa chặt API
# #     if not is_presentation_time():
# #         return f"💡 Chế độ {current_mode}: Hệ thống đang hoạt động ổn định. (AI đang ngủ đông để tiết kiệm Quota)."

# #     current_time_sec = time.time()

# #     # 2. Kiểm tra thời gian chờ (Cooldown)
# #     if os.path.exists(TIME_FILE) and os.path.exists(CACHE_FILE):
# #         with open(TIME_FILE, "r") as f:
# #             try:
# #                 last_call = float(f.read().strip())
# #                 if current_time_sec - last_call < COOLDOWN_SECONDS:
# #                     # Chưa đủ 2 phút -> Đọc ngay câu cũ trong cache ra hiển thị
# #                     with open(CACHE_FILE, "r", encoding="utf-8") as cache:
# #                         return cache.read()
# #             except ValueError:
# #                 pass

# #     # 3. VÁ LỖI: Cập nhật thời gian khóa NGAY LẬP TỨC trước khi gọi API để chống spam khi lỗi
# #     with open(TIME_FILE, "w") as f:
# #         f.write(str(current_time_sec))

# #     # 4. Tiến hành gọi AI Google Gemini
# #     try:
# #         print(f"[AI Trigger] Chuyển đổi hợp lệ: Đang gọi Gemini lấy lời khuyên cho chế độ {current_mode}...")
        
# #         # --- ĐOẠN CODE GỌI GEMINI GỐC CỦA BẠN ---
# #         prompt = f"Hệ thống nhà kính đang ở chế độ: {current_mode}. Hãy cho một lời khuyên ngắn gọn bằng tiếng Nhật hoặc tiếng Việt."
# #         # model = genai.GenerativeModel('gemini-2.0-flash')
# #         # response = model.generate_content(prompt)
# #         # ai_response = response.text
        
# #         # (Đây là biến chứa kết quả thật sau khi gọi thành công, thay bằng response.text của bạn)
# #         ai_response = f"💡 Chế độ {current_mode}: Lời khuyên tối ưu từ chuyên gia AI..." 
        
# #         # Nếu gọi thành công, lưu đè vào file Cache để dùng cho các lần sau
# #         with open(CACHE_FILE, "w", encoding="utf-8") as f:
# #             f.write(ai_response)
            
# #         return ai_response
        
# #     except Exception as e:
# #         print(f"[AI Lỗi hệ thống] Gặp lỗi gọi API nhưng đã được kích hoạt khiên cứu cánh: {str(e)}")
# #         # NẾU LỖI (429 hoặc rớt mạng): Lập tức đọc câu cũ trong Cache ra trả về cho Web cứu cánh
# #         if os.path.exists(CACHE_FILE):
# #             with open(CACHE_FILE, "r", encoding="utf-8") as cache:
# #                 return cache.read()
# #         return f"💡 Chế độ {current_mode}: Hệ thống thông minh đang phân tích dữ liệu cảm biến..."
    
# #     import time
# # from datetime import datetime, time as datetime_time

# def is_presentation_time():
#     # Luôn trả về True để bạn test lúc nào cũng được
#     return True

# def get_pro_advice(current_mode):
#     # Trả về lời khuyên tương ứng với trạng thái nhà kính ngay lập tức (Không tốn 1 giọt Quota nào)
#     if current_mode == "SUNNY":
#         return "💡 [Chuyên gia AI] Trời nắng gắt (Nhiệt độ tăng). Hệ thống đã chủ động ĐÓNG mái che và kích hoạt phun sương để hạ nhiệt, bảo vệ độ ẩm cho cây."
#     elif current_mode == "CLOUDY":
#         return "💡 [Chuyên gia AI] Trời nhiều mây, ánh sáng giảm. Hệ thống đã MỞ mái che để tối ưu hóa hấp thụ ánh sáng tự nhiên cho quá trình quang hợp."
#     elif current_mode == "NIGHT":
#         return "💡 [Chuyên gia AI] Hệ thống chuyển sang chế độ ban đêm. Đang duy trì trạng thái nghỉ ngơi ổn định cho cây trồng."
#     else:
#         return f"💡 [Chuyên gia AI] Nhà kính đang ở chế độ {current_mode}. Hệ thống đang giám sát các chỉ số cảm biến liên tục."





import os
import sqlite3
import time
from datetime import datetime, time as datetime_time
from dotenv import load_dotenv

# =====================================================================
# KHU VỰC CODE CŨ (ĐÃ ĐÓNG BĂNG ĐỂ TRÁNH LỖI HẾT QUOTA GOOGLE)
# Chú ý: Không xóa, chỉ comment lại để dành cho tương lai.
# =====================================================================

# import google.generativeai as genai

# Nạp các biến môi trường từ file .env vào hệ thống ngầm
# load_dotenv()      

# Lấy API Key một cách an toàn từ môi trường
# api_key = os.getenv("GEMINI_API_KEY2")

# Cấu hình API Key bảo mật cho Gemini
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel('gemini-2.0-flash')

# def get_ai_advice():
#     conn = sqlite3.connect("greenhouse_data.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT temperature, humidity FROM sensor_logs ORDER BY id DESC LIMIT 10")
#     rows = cursor.fetchall()
#     conn.close()
#     
#     prompt = f"Dữ liệu 10 lần đo gần nhất (nhiệt độ, độ ẩm): {rows}. Hãy đưa ra lời khuyên ngắn (dưới 50 từ) chăm sóc cây."
#     
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except:
#         return "AI đang bận, thử lại sau nhé!"

# def generate_professional_advice(mode, temp, hum, light):
#     persona = """...""" # (Đã ẩn bớt cho gọn)
#     prompt = f"""..."""
#     try:
#         response = model.generate_content(prompt)
#         return response.text
#     except:
#         return "Lỗi"

# ADVICE_MESSAGES = {
#     "R_DAY": "雨が降ってきたので、自動で屋根を閉じました！☔ 植物たちは安全だよ！✨",
#     "R_NIGHT": "雨の夜モードです！🌙🌧️ 温度を守るために屋根を閉じました。すべて順調だよ！✨",
#     "SUNNY": "ピカピカの晴れです！☀️ お日さまの光がたっぷりで、植物たちも大喜びだよ！🚀",
#     "CLOUDY": "今は曇り空です☁️ お日さまは隠れているけど、みんな元気だよ！🌱",
#     "NIGHT": "静かな夜モードです！🌙 温湿度もばっちりで、植物たちのおやすみタイムだよ💤"
# }

# def get_ai_transition_analysis(mode, temp, hum, light):
#    ...

# if __name__ == "__main__":
#     advice = get_ai_advice()
#     with open("ai_advice.txt", "w", encoding="utf-8") as f:
#         f.write(advice)

# CACHE_FILE = "ai_advice_cache.txt"
# TIME_FILE = "last_ai_time.txt"
# COOLDOWN_SECONDS = 120 


# =====================================================================
# KHU VỰC CODE CHÍNH THỨC CHO BUỔI THUYẾT TRÌNH (CHẠY OFFLINE)
# Cơ chế giả lập tốc độ cao, không phụ thuộc vào Internet hay Google
# =====================================================================

def is_presentation_time():
    # Luôn trả về True để hệ thống hoạt động bất kể lúc nào bạn test và thuyết trình
    return True

import random

def get_pro_advice(current_mode, previous_mode=None, temp=25.0, hum=75.0, light=0.85):
    # Kho dữ liệu lời khuyên cho từng cặp chuyển đổi
    # Cấu trúc: [ "Câu 1", "Câu 2", "Câu 3", "Câu 4", "Câu 5" ]
    ADVICE_DB = {
        ("SUNNY", "CLOUDY"): [
            "曇り空ですね☁️ 屋根を開けて自然の風を届けます！｜Trời nhiều mây rồi! Mở mái che đón gió tự nhiên thôi nào!✨",
            "光を調整中！植物たちはリラックスしています🌱｜Đang điều chỉnh ánh sáng! Các em cây đang thư giãn lắm đấy!🌱",
            "曇りの日は植物の休息時間☁️ 屋根開放！｜Trời mây là thời gian nghỉ ngơi của cây! Mở mái che ngay!🚀",
            "心地よい曇り空です☁️ 快適な環境を維持中！｜Một ngày nhiều mây thật dễ chịu! Hệ thống vẫn giữ môi trường ổn định!✨",
            "お日さまが隠れても管理は完璧！☁️｜Dù nắng bị che khuất, việc quản lý vẫn hoàn hảo!🔥"
        ],
        ("SUNNY", "R_DAY"): [
            "雨が来ました！☔ 屋根を閉じてガード完了！｜Mưa đến rồi! Đã đóng mái bảo vệ an toàn!☔",
            "雨宿りタイムです！☔ 内部はとっても快適！｜Thời gian trú mưa thôi! Bên trong nhà kính đang rất thoải mái!✨",
            "恵みの雨！☔ 屋根を閉めて湿度を守ります！｜Cơn mưa ban phước! Đóng mái để giữ độ ẩm ổn định!🚀",
            "雨の日でも植物は元気いっぱい！☔｜Dù trời mưa, cây cối vẫn tràn đầy năng lượng!🌱",
            "雨対策OK！☔ 内部の植物たちは幸せそう！｜Chống mưa đã sẵn sàng! Các em cây đang rất hạnh phúc!🔥"
        ],
        ("R_DAY", "SUNNY"): [
            "晴れ間が見えてきました！☀️ 屋根を開けて光を届けよう！｜Nắng lên rồi! Mở mái che đón ánh sáng thôi!✨",
            "雨が止んで最高の天気です！☀️ 光合成スタート！｜Mưa tạnh rồi, thời tiết tuyệt vời! Bắt đầu quang hợp thôi!🚀",
            "太陽が戻ってきた！☀️ 植物たちも大喜びだよ！｜Mặt trời quay lại rồi! Các em cây đang vui sướng lắm!🔥",
            "晴れ！☀️ 風通しを良くして気分転換！｜Nắng rồi! Lưu thông không khí để cây thay đổi không khí nào!🌱",
            "最高の晴れ日和！☀️ どんどん成長しよう！｜Ngày nắng tuyệt vời! Cùng lớn nhanh nào!✨"
        ],
        ("CLOUDY", "R_DAY"): [
            "雨が降り始めました☔ 慌てず屋根を閉鎖！｜Mưa bắt đầu rơi rồi! Bình tĩnh đóng mái che lại nhé!☔",
            "雨雲が来ましたね☔ 植物を守り抜きます！｜Mây mưa đến rồi! Hệ thống sẽ bảo vệ cây cối đến cùng!✨",
            "雨音を聞きながら、温室を守ります☔｜Vừa nghe tiếng mưa, vừa bảo vệ nhà kính!🚀",
            "雨対策開始！☔ 植物たちは雨宿りだよ！｜Bắt đầu chống mưa! Các em cây đang trú mưa an toàn!🌱",
            "雨が来たね！☔ 内部はしっとり快適です！｜Mưa đến rồi! Không gian bên trong đang rất dễ chịu!🔥"
        ],
        ("CLOUDY", "SUNNY"): [
            "太陽が顔を出しました！☀️ 屋根を開けて光を浴びよう！｜Mặt trời xuất hiện rồi! Mở mái đón nắng thôi!✨",
            "晴れました！☀️ 植物たちのエネルギーを全開に！｜Nắng rồi! Nạp đầy năng lượng cho cây thôi nào!🚀",
            "最高の天気です！☀️ 光合成の準備はいい？｜Thời tiết tuyệt nhất! Đã sẵn sàng quang hợp chưa?🔥",
            "晴れの日モード！☀️ どんどん元気になるよ！｜Chế độ ngày nắng! Các em cây sẽ khỏe mạnh hơn đấy!🌱",
            "お日さまがパワーをくれる！☀️ 成長のチャンス！｜Ánh mặt trời mang lại sức mạnh! Cơ hội để lớn nhanh!✨"
        ],
        ("NIGHT", "R_NIGHT"): [
            "夜の雨だね☔ 屋根をしっかり閉じてます！｜Mưa đêm rồi! Mái che đã đóng chặt rồi nhé!☔",
            "雨の夜も温室は安全です！🌙☔｜Dù mưa đêm, nhà kính vẫn rất an toàn!✨",
            "夜の雨、植物は夢の中🌙☔ 安全第一！｜Mưa đêm, cây đang trong giấc mơ! An toàn là trên hết!🚀",
            "雨音が眠りを誘う夜です🌙☔ 管理OK！｜Tiếng mưa ru ngủ trong đêm! Quản lý vẫn tốt!🌱",
            "雨の夜のガード完了！🌙☔ おやすみなさい！｜Đã bảo vệ xong trong đêm mưa! Ngủ ngon nhé!🔥"
        ],
        ("R_NIGHT", "NIGHT"): [
            "雨が止んで静かな夜🌙 星が見えてきたよ！｜Mưa tạnh rồi, một đêm tĩnh lặng! Sao đã bắt đầu hiện ra!✨",
            "雨上がりの夜です🌙 植物たちもお休み中！｜Đêm sau mưa! Các em cây đang nghỉ ngơi!🚀",
            "静かな夜モードへ🌙 湿度も完璧に管理中！｜Chuyển sang chế độ đêm tĩnh lặng! Độ ẩm đang được quản lý hoàn hảo!🔥",
            "雨も止んで、良い夢が見れそう🌙🌱｜Mưa tạnh rồi, chúc cây có giấc mơ đẹp!🌱",
            "夜の静寂🌙 システムは常に植物を見守ります！｜Sự tĩnh lặng của đêm! Hệ thống luôn dõi theo cây cối!✨"
        ]
    }

    

    # 1. GHI LOG ĐỂ BIẾT NÓ ĐANG TÌM CẶP NÀO
    print(f"[DEBUG AI] Tìm kiếm cặp: ({previous_mode}, {current_mode})")
    
    # 2. Ưu tiên lấy theo cặp
    if previous_mode and (previous_mode, current_mode) in ADVICE_DB:
        content = random.choice(ADVICE_DB[(previous_mode, current_mode)])
        jp, vn = content.split("｜")
        return f"{jp}\n{vn}"
    
    # Trả về câu theo chế độ hiện tại
    return "データを分析中です..."
def get_ai_transition_analysis(mode, temp, hum, light):
    # Thay vì gọi Gemini, ta gọi hàm giả lập phía trên
    
    return get_pro_advice(mode)