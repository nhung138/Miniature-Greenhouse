import time
from datetime import datetime
from config import CONFIG
import os
import sys
import subprocess
from database import init_db, log_data
from ai_consultant import get_pro_advice
import requests
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

# Import tất cả các module linh kiện
from modules.sensors.dht_sensor import DHTManager       
from modules.sensors.light_sensor import LightSensorManager
from modules.actuators.rgb_led import RGBManager
from modules.actuators.servo import ServoManager
from modules.display.lcd_pcf8574 import LCDManager

def get_system_mode(light_val, temp, hum, force_hour=None):
    # TÍNH TOÁN THỜI GIAN
    hour = force_hour if force_hour is not None else datetime.now().hour
    is_night = (hour >= 18 or hour < 6)
    
    # CÁC NGƯỠNG CÀI ĐẶT
    H_RAIN_THRESHOLD = 90.0  
    LIGHT_SUNNY_THRESHOLD = 0.70
    
    # 1. Kiểm tra MƯA
    if hum >= H_RAIN_THRESHOLD:
        return ("R_NIGHT" if is_night else "R_DAY"), "CLOSE"
        
    # 2. Kiểm tra ĐÊM
    if is_night:
        return "NIGHT", "CLOSE"
        
    # 3. Kiểm tra NẮNG/MÂY
    if light_val >= LIGHT_SUNNY_THRESHOLD:
        return "SUNNY", "CLOSE"
    else:
        return "CLOUDY", "OPEN"

def run_normal_mode(forced_hour=None):
    init_db()

    print("\nĐang khởi tạo hệ thống cảm biến...")
    
    dht = DHTManager()
    ldr = LightSensorManager()
    rgb = RGBManager()
    servo = ServoManager()
    lcd = LCDManager()

    # Hiển thị màn hình chào mừng
    lcd.show_welcome()
    print("Hiển thị màn hình chào mừng...")
    time.sleep(3)

    print("Hệ thống bắt đầu giám sát môi trường tự động!\n")
    error_count = 0
    last_mode = None
    
    try:
        while True:
            # 🌟 GIẢI PHÁP 1: ÉP PYTHON ĐỌC LẠI TIMEZONE MỚI TỪ OS TRÊN MỖI CHU KỲ
            try:
                time.tzset()
            except AttributeError:
                pass # Bỏ qua nếu chạy thử nghiệm trên Windows/macOS

            # BƯỚC 1: ĐỌC DỮ LIỆU CẢM BIẾN TRƯỚC
            temp, hum = dht.read()
            light_val = ldr.read_value() 

            # BƯỚC 2: XỬ LÝ LỖI CẢM BIẾN (FAILSAFE)
            if temp is None or light_val is None:
                error_count += 1
                print(f"Cảnh báo: Lỗi đọc cảm biến! ({error_count}/{CONFIG['FAILSAFE']['MAX_ERRORS']})")
                
                # Gửi trạng thái lỗi tạm thời lên API để cập nhật giao diện Web
                try:
                    requests.post("http://localhost:8000/update-state", json={
                        "mode": "UNKNOWN",
                        "temp": 0.0,
                        "hum": 0.0
                    }, timeout=1)
                except:
                    pass

                if error_count >= CONFIG["FAILSAFE"]["MAX_ERRORS"]:
                    print("LỖI NGHIÊM TRỌNG: Khóa hệ thống an toàn!")
                    rgb.set_color("OFF")           
                    servo.close()                  
                    lcd.show_alert("SYSTEM LOCKED!") 
                    break                          
                
                time.sleep(1)
                continue
            else:
                error_count = 0 

            # BƯỚC 3: QUYẾT ĐỊNH CHẾ ĐỘ KHI ĐÃ CÓ ĐỦ DỮ LIỆU
            mode, roof_txt = get_system_mode(light_val, temp, hum, forced_hour)
            
            # BƯỚC 4: GỬI TRẠNG THÁI MỚI LÊN API NGAY LẬP TỨC
            try:
                requests.post("http://localhost:8000/update-state", json={
                    "mode": mode,
                    "temp": temp,
                    "hum": hum
                }, timeout=1)
            except Exception as api_err:
                # Tránh làm sập chương trình phần cứng nếu API mất kết nối tạm thời
                print(f"[API Error] Không thể đồng bộ dữ liệu lên Web: {api_err}")

            # BƯỚC 5: XỬ LÝ LỜI KHUYÊN HỆ THỐNG / AI
            if mode != last_mode:
                advice = get_pro_advice(mode) # Lấy lời khuyên chính xác từ dictionary
                with open("ai_advice.txt", "w", encoding="utf-8") as f:
                    f.write(advice)
                print(f"[Hệ thống] Chế độ {mode} - Đã cập nhật lời khuyên mới.")
                last_mode = mode

            # BƯỚC 6: ĐIỀU KHIỂN PHẦN CỨNG NGOẠI VI
            rgb.set_color(mode)
            if roof_txt == "OPEN":
                servo.open()
            else:
                servo.close()
            
            # Lưu log (Lúc này hàm log_data lấy thời gian từ SQLite sẽ ăn theo Timezone mới)
            log_data(temp, hum, light_val, mode)
            lcd.display_data(temp, hum, light_val, mode, roof_txt)
            print(f"[{mode}] Nhiệt: {temp}°C | Ẩm: {hum}% | Sáng: {light_val:.2f} | Mái: {roof_txt}")
            
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[!] Đã nhận lệnh dừng chương trình.")
        # Dọn dẹp trạng thái thiết bị khi thoát
        lcd.clear()
        rgb.set_color("OFF")
        servo.close()
        print("Hệ thống đã tắt.")

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print("HỆ THỐNG NHÀ KÍNH MINI - MINIATURE GREENHOUSE")
    print("=> [Thực tế] Tự động kích hoạt Chế độ Thực tế...")
    print("=> [Thực tế] Đang sử dụng giờ hệ thống...")
    
    # Chạy thẳng chế độ thực tế với giờ mặc định của hệ thống (forced_hour = None)
    run_normal_mode(forced_hour=None)

# if __name__ == "__main__":
#     os.system('clear' if os.name == 'posix' else 'cls')
    
#     print("HỆ THỐNG NHÀ KÍNH MINI - MINIATURE GREENHOUSE")
    
#     # --- PHẦN SỬA LỖI EOFError (Tự động hóa) ---
#     # Kiểm tra tham số từ command line: main.py [chế_độ] [thời_gian]
#     if len(sys.argv) >= 3:
#         choice = sys.argv[1]
#         time_choice = sys.argv[2]
#         print(f"Khởi động tự động: Chế độ {choice}, Thời gian {time_choice}")
#     else:
#         # Chạy thủ công
#         print("\n Vui lòng chọn chế độ khởi động:")
#         print("   [1] Chế độ Thực tế (Đọc cảm biến tự động)")
#         print("   [2] Chế độ Giả lập (Test phần cứng)")
#         choice = input("Nhập lựa chọn của bạn (1 hoặc 2): ").strip()
        
#         if choice == '1':
#             print("\n--- CẤU HÌNH THỜI GIAN ---")
#             print("   [0] Thời gian thực tế")
#             print("   [1] Giả lập Ban ngày (10h sáng)")
#             print("   [2] Giả lập Ban đêm (20h tối)")
#             time_choice = input("Chọn thời gian (0/1/2): ").strip()
#         else:
#             time_choice = '0'

#     # --- LOGIC KHỞI ĐỘNG ---
#     if choice == '1':
#         forced_hour = None
#         if time_choice == '1': 
#             forced_hour = 10
#             print("=> [Giả lập] Bắt đầu với giờ: 10:00")
#         elif time_choice == '2': 
#             forced_hour = 20
#             print("=> [Giả lập] Bắt đầu với giờ: 20:00")
#         else:
#             print("=> [Thực tế] Đang sử dụng giờ hệ thống...")
        
#         run_normal_mode(forced_hour)
            
#     elif choice == '2':
#         print("=> Bắt đầu nạp Chế độ Giả lập...")
#         try:
#             import mock_main
#             mock_main.test_system()
#         except ImportError:
#             print("❌ LỖI: Không tìm thấy file 'mock_main.py'.")
#     else:
#         print("❌ Lựa chọn không hợp lệ!")