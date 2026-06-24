from RPLCD.i2c import CharLCD
from config import CONFIG
import time

class LCDManager:
    def __init__(self):
        self.lcd = CharLCD(
            i2c_expander='PCF8574', 
            address=CONFIG["LCD"]["ADDRESS"], 
            port=1, 
            cols=CONFIG["LCD"]["COLS"], 
            rows=CONFIG["LCD"]["ROWS"]
        )
        # Nạp các biểu tượng tự vẽ vào bộ nhớ của LCD
        self._create_custom_icons()

    def _create_custom_icons(self):
        """Vẽ các biểu tượng thời tiết (0-4) và biểu tượng chào mừng (5)"""
        sun = (0b00100, 0b10101, 0b01110, 0b11111, 0b01110, 0b10101, 0b00100, 0b00000)
        cloud = (0b00000, 0b00000, 0b01110, 0b11111, 0b11111, 0b00000, 0b00000, 0b00000)
        rain = (0b01110, 0b11111, 0b11111, 0b00000, 0b10101, 0b01010, 0b10101, 0b00000)
        moon = (0b00111, 0b01100, 0b11000, 0b11000, 0b11000, 0b01100, 0b00111, 0b00000)
        rain_night = (0b01100, 0b11000, 0b11000, 0b00000, 0b10101, 0b01010, 0b10101, 0b00000)
        cute_heart = (0b00000, 0b01010, 0b10101, 0b10001, 0b01010, 0b00100, 0b00000, 0b00000)

        self.lcd.create_char(0, sun)
        self.lcd.create_char(1, cloud)
        self.lcd.create_char(2, rain)
        self.lcd.create_char(3, moon)
        self.lcd.create_char(4, rain_night)
        self.lcd.create_char(5, cute_heart) 

    def show_welcome(self):
        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(f" Hello! {chr(5)} {chr(5)} {chr(5)}")
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string("MINI GREENHOUSE")

    def display_data(self, temp, hum, light_val, mode, roof):
        # Chuyển thành float để giữ lại phần thập phân (vd: 24.2)
        t_val = float(temp) if temp is not None else 0.0
        h_val = float(hum) if hum is not None else 0.0
        l_val = float(light_val) if light_val is not None else 0.0
        
        # Mapping các biểu tượng chế độ
        icon_id = 0
        if mode == "SUNNY":       icon_id = 0
        elif mode == "CLOUDY":    icon_id = 1
        elif mode == "RAINY_DAY": icon_id = 2
        elif mode == "NIGHT":     icon_id = 3
        elif mode == "RAINY_NIGHT": icon_id = 4

        # Dòng 1: T:{Nhiệt độ}.1f°C H:{Độ ẩm}.1f% (Vừa đúng 16 ký tự)
        # Sử dụng chr(223) để in ký hiệu độ (°) chuẩn trên LCD 16x2
        row_0 = f"T:{t_val:.1f}{chr(223)}C H:{h_val:.1f}%"
        
        # Dòng 2: Icon, Chế độ và Ánh sáng dạng thập phân (0.00)
        mode_str = f"{chr(icon_id)}{mode}"
        light_str = f"L:{l_val:.2f}"
        
        # Tính toán khoảng trắng ở giữa để đẩy `light_str` sát mép phải LCD
        space_count = 16 - len(mode_str) - len(light_str)
        spaces = " " * (space_count if space_count > 0 else 1)
        row_1 = f"{mode_str}{spaces}{light_str}"

        self.lcd.clear()
        self.lcd.cursor_pos = (0, 0)
        self.lcd.write_string(row_0[:16]) 
        self.lcd.cursor_pos = (1, 0)
        self.lcd.write_string(row_1[:16])

    def show_alert(self, msg):
        self.lcd.clear()
        self.lcd.write_string(msg[:16])

    def clear(self):
        self.lcd.clear()