from gpiozero import Servo, LED
from gpiozero.pins.lgpio import LGPIOFactory
from config import CONFIG
import time

class ServoManager:
    def __init__(self):
        factory = LGPIOFactory()
        self.servo = Servo(
            CONFIG["GPIO"]["SERVO"],
            min_pulse_width=0.5/1000, 
            max_pulse_width=2.5/1000,
            pin_factory=factory,
            initial_value=None
        )
        # Khởi tạo đèn LED báo trạng thái mái che ở đây
        self.servo_led = LED(CONFIG["GPIO"]["SERVO_LED"])
        
        self.current_pos = None # Ghi nhớ vị trí
        self.servo.detach()
    
    def open(self):
        """Mở mái che và bật đèn LED báo hiệu"""
        if self.current_pos == True:
            return
            
        self.servo.max()
        self.servo_led.on()     # Bật LED khi mái che mở
        
        self.current_pos = True
        time.sleep(0.5)
        self.servo.detach()

    def close(self):
        """Đóng mái che và tắt đèn LED báo hiệu"""
        if self.current_pos == False:
            return
            
        self.servo.min()
        self.servo_led.off()    # Tắt LED khi mái che đóng
        
        self.current_pos = False
        time.sleep(0.5)
        self.servo.detach()