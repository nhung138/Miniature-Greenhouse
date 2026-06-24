# from config import CONFIG
# import spidev 

# class LightSensorManager: 
#     def __init__(self):
#         self.spi = spidev.SpiDev()
#         self.spi.open(0, 0) # Mở SPI bus 0, device 0
#         self.spi.max_speed_hz = 1350000

#     def read_lux(self):
#         # Logic đọc dữ liệu từ cảm biến ánh sáng
#         # Đây chỉ là ví dụ, bạn hãy điền logic của bạn vào đây
#         return 1500 # Trả về giá trị giả lập để test

import spidev 
from config import CONFIG

class LightSensorManager: 
    def __init__(self):
        # Khởi tạo giao tiếp SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0) # Mở SPI bus 0, device 0 (tương ứng với chân CE0)
        self.spi.max_speed_hz = 1350000
        
        # MCP3208 có 8 kênh (CH0 đến CH7). Sơ đồ của bạn cắm vào CH0.
        self.channel = 0 

    def read_value(self):
        """
        Đọc dữ liệu Analog từ MCP3208.
        Do MCP3208 là chip 12-bit, giá trị thô sẽ từ 0 - 4095.
        Hàm này trả về giá trị đã chuẩn hóa: 0.0 (Tối) đến 1.0 (Sáng).
        """
        try:
            # Gửi 3 byte lệnh qua SPI để yêu cầu chip MCP3208 đọc kênh CH0
            # Công thức chuẩn cho MCP3208 (Single-Ended)
            adc_response = self.spi.xfer2([6 | (self.channel >> 2), (self.channel & 3) << 6, 0])
            
            # Chip trả về 3 byte, chúng ta ghép 4 bit cuối của byte[1] và toàn bộ byte[2]
            raw_value = ((adc_response[1] & 15) << 8) + adc_response[2]
            
            # Chuẩn hóa về thang 0.0 - 1.0
            normalized_value = raw_value / 4095.0
            
            # LƯU Ý: Tùy vào cách bạn nối điện trở cho LDR trên Breadboard.
            # Nếu chạy thử thấy trời Tối mà nó báo 1.0, trời Sáng báo 0.0 (Bị ngược)
            # Thì bạn đổi dòng return thành: return 1.0 - normalized_value
            
            return normalized_value
            
        except Exception as e:
            print(f"Lỗi phần cứng khi đọc SPI (MCP3208): {e}")
            return None