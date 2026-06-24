from gpiozero import RGBLED
from config import CONFIG

class RGBManager:
    def __init__(self):
        pins = CONFIG["GPIO"]["RGB"]
        self.led = RGBLED(red=pins["R"], green=pins["G"], blue=pins["B"])

    

    def set_color(self, mode):
        # Chế độ SUNNY: Nắng gắt -> ĐÓNG mái che để che nắng
        if mode == "SUNNY":
            self.led.color = (1, 0, 0.3)       # RGB Vàng
            #self.servo.close()               
            #self.servo_led.off()             
            
        # Chế độ CLOUDY: Trời mát mẻ -> MỞ mái che đón gió và sáng
        elif mode == "CLOUDY":
            self.led.color = (0, 1, 0)       # RGB Xanh dương
            #self.servo.open()                
            #self.servo_led.on()              # Mở mái che thì sáng đèn LED trạng thái
            
        # Chế độ RAINY_DAY: Mưa ban ngày -> ĐÓNG mái che che mưa
        elif mode == "R_DAY":
            self.led.color = (0.2, 0.2, 0.2) # RGB Trắng xám
            #self.servo.close()               
            #self.servo_led.off()             
            
        # Chế độ NIGHT: Đêm tĩnh mịch -> ĐÓNG mái che giữ ấm
        elif mode == "NIGHT":
            self.led.color = (1, 0.5, 0)   # RGB Tím
            #self.servo.close()               
            #self.servo_led.off()             
            
        # Chế độ RAINY_NIGHT: Đêm mưa lạnh -> ĐÓNG mái che
        elif mode == "R_NIGHT":
            self.led.color = (0.2, 0.25, 0.05)   # RGB Xanh úa (Dark Olive)
            #self.servo.close()               
            #self.servo_led.off()             
            
        # Trạng thái lỗi hoặc chưa xác định -> Tắt toàn bộ để an toàn
        else:
            self.led.off()
            #self.servo.close()
            #self.servo_led.off()