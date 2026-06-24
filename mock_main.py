import os
import time

# Cấu hình GPIO cho Raspberry Pi 5
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

# Import các Module thực tế (đảm bảo hệ thống chạy thật)
from modules.actuators.rgb_led import RGBManager
from modules.actuators.servo import ServoManager
from modules.display.lcd_pcf8574 import LCDManager

# Định nghĩa màu sắc Terminal để dễ theo dõi
CYAN = '\033[96m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
WHITE = '\033[97m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def get_system_mode(light_val, temp, hum):
    """
    Thuật toán điều khiển dựa trên thiết kế hệ thống của bạn:
    SUNNY, CLOUDY, R_DAY, R_NIGHT, NIGHT
    """
    if light_val > 0.85:
        if temp > 23 and hum > 50:
            return "SUNNY", "CLOSE", YELLOW
        else:
            return "CLOUDY", "OPEN", GREEN
    elif light_val >= 0.55:
        if hum >= 85:
            return "R_DAY", "CLOSE", WHITE
        else:
            return "CLOUDY", "OPEN", GREEN
    else:
        if temp <= 23 and hum >= 85:
            return "R_NIGHT", "CLOSE", CYAN
        else:
            return "NIGHT", "CLOSE", MAGENTA

def print_season_hint(season_choice):
    print(f"\n{CYAN}--- BẢNG GỢI Ý MÔI TRƯỜNG ---{RESET}")
    hints = {
        '1': "Mùa Xuân (Nồm)   : Nhiệt 20-25°C | Ẩm 85-98% | Sáng 0.5-0.7",
        '2': "Mùa Hạ (Nóng)    : Nhiệt 28-40°C | Ẩm 55-75% | Sáng 0.8-1.0",
        '3': "Mùa Thu (Mát)    : Nhiệt 20-26°C | Ẩm 50-70% | Sáng 0.6-0.8",
        '4': "Mùa Đông (Lạnh)  : Nhiệt 10-18°C | Ẩm 40-60% | Sáng 0.1-0.4"
    }
    print(hints.get(season_choice, ""))
    print(f"{CYAN}--------------------------{RESET}\n")

def run_mock_system():
    # Khởi tạo phần cứng
    rgb, servo, lcd = RGBManager(), ServoManager(), LCDManager()
    
    # Màn hình chào mừng
    lcd.show_welcome() 
    time.sleep(2)

    try:
        while True:
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"{GREEN}=== MÔ PHỎNG HỆ THỐNG GIẢM SÁT MÔI TRƯỜNG ==={RESET}")
            print("1. Xuân | 2. Hạ | 3. Thu | 4. Đông | 5. Thoát")
            
            choice = input("\nChọn mùa để giả lập: ").strip()
            if choice == '5': break
            if choice not in ['1', '2', '3', '4']: continue
            
            print_season_hint(choice)
            
            # NHẬP LIỆU VỚI CƠ CHẾ KIỂM TRA LỖI (VALIDATION)
            try:
                temp = float(input("Nhập Nhiệt độ (°C): "))
                if not (-10 <= temp <= 60): raise ValueError("Nhiệt độ ngoài tầm đo!")
                
                hum = float(input("Nhập Độ ẩm (%): "))
                if not (0 <= hum <= 100): raise ValueError("Độ ẩm không hợp lệ!")
                
                light = float(input("Nhập Ánh sáng (0.0-1.0): "))
                if not (0.0 <= light <= 1.0): raise ValueError("Ánh sáng ngoài tầm đo!")
                
                # Xử lý logic
                mode, roof, color = get_system_mode(light, temp, hum)
                
                # Điều khiển phần cứng thật
                rgb.set_color(mode)
                servo.open() if roof == "OPEN" else servo.close()
                lcd.display_data(temp, hum, light, mode, roof)
                
                print(f"\n{color}>> Kịch bản: {mode} | Mái: {roof}{RESET}")
                input("\nNhấn Enter để tiếp tục...")
                
            except ValueError as e:
                print(f"{RED}Dữ liệu lỗi: {e}{RESET}")
                time.sleep(2)

    finally:
        # Lời chào tạm biệt
        lcd.clear()
        lcd.lcd.cursor_pos = (0, 0)
        lcd.lcd.write_string("   THANK YOU!   ")
        lcd.lcd.cursor_pos = (1, 0)
        lcd.lcd.write_string(" SEE YOU LATER! ")
        
        rgb.set_color("OFF")
        servo.close()
        time.sleep(3)
        lcd.clear()
        print("Đã đóng hệ thống an toàn.")

if __name__ == "__main__":
    run_mock_system()