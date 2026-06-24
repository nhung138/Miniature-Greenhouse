# Miniature Greenhouse - Hệ thống Nhà kính Thông minh

Dự án này là giải pháp tự động hóa nhà kính thu nhỏ, sử dụng Raspberry Pi để giám sát môi trường và tự động điều khiển các cơ cấu chấp hành (Servo, LED RGB, Màn hình LCD), đảm bảo điều kiện sống tối ưu cho cây trồng.

Đặc biệt, hệ thống được trang bị 2 chế độ vận hành linh hoạt: Đọc cảm biến tự động (Thực tế) và Mô phỏng kịch bản (Giả lập phần cứng).

## 1. Cấu trúc hệ thống
Hệ thống vận hành theo cơ chế vòng lặp liên tục:

Thu thập dữ liệu cảm biến (Nhiệt độ, Độ ẩm, Cường độ sáng 0.0 - 1.0) → Kiểm tra ngưỡng (Thresholds) → Kích hoạt thiết bị chấp hành (Mở/Đóng mái che, Đổi màu đèn cảnh báo, Hiển thị LCD).


## 2. Logic vận hành chi tiết
## 🌤️ Kịch bản Hoạt động (5 Chế độ Thời tiết)

Hệ thống phân tích mức độ ánh sáng (đọc qua bộ chuyển đổi ADC) thay vì thời gian thực, kết hợp với Nhiệt độ và Độ ẩm để đưa ra quyết định bảo vệ cây trồng.

 Dưới đây là 5 kịch bản tự động của hệ thống:

### 1. ☀️ Chế độ Nắng gắt (SUNNY)
* Điều kiện: Ánh sáng mạnh (> 0.85), Nhiệt độ > 23°C & Độ ẩm > 50%.
* Hành động phần cứng:
  * Mái che (Servo): ĐÓNG (Tắt LED trạng thái).
  * Đèn cảnh báo (RGB): Sáng màu Vàng.
  * Màn hình (LCD): Hiển thị SUNNY
* Mục đích nông nghiệp: Cản bức xạ nhiệt trực tiếp, chống sốc nhiệt, ngăn chặn tình trạng mất nước bốc hơi nhanh và cháy lá cây.

### 2. ☁️ Chế độ Nắng dịu / Nhiều mây (CLOUDY)
* Điều kiện: Ban ngày (06h - 17h), ánh sáng vừa (0.55 đến 0.85) hoặc sáng mạnh nhưng nhiệt độ mát mẻ/độ ẩm thấp.
* Hành động phần cứng:
  * Mái che (Servo): MỞ (Bật sáng LED trạng thái).
  * Đèn cảnh báo (RGB): Sáng màu Xanh dương.
  * Màn hình (LCD): Hiển thị CLOUDY!
* Mục đích nông nghiệp: Tận dụng tối đa nguồn sáng tự nhiên và gió lùa, giúp cây đẩy mạnh quá trình quang hợp và phát triển.

### 3. 🌧️ Chế độ Mưa ban ngày (RAINY DAY)
* Điều kiện: Ban ngày (06h - 17h), ánh sáng âm u (0.55 <= light <= 0.85), Độ ẩm không khí cao (>= 85%).
* Hành động phần cứng:
  * Mái che (Servo): ĐÓNG (Tắt LED trạng thái).
  * Đèn cảnh báo (RGB): Sáng màu Trắng xám.
  * Màn hình (LCD): Hiển thị R_DAY!.
* Mục đích nông nghiệp: Che chắn kịp thời để tránh mưa lớn gây ngập úng thối gốc, xói mòn bề mặt đất và rửa trôi phân bón.

### 4. 🌙 Chế độ Đêm tĩnh mịch (NIGHT)
* Điều kiện: Ban đêm (18h - 05h), ánh sáng yếu/tắt hoàn toàn (< 0.55), điều kiện nhiệt độ và độ ẩm bình thường.
* Hành động phần cứng:
  * Mái che (Servo): ĐÓNG (Tắt LED trạng thái).
  * Đèn cảnh báo (RGB): Sáng màu Tím.
  * Màn hình (LCD): Hiển thị NIGHT!
* Mục đích nông nghiệp: Hoạt động như một lớp màng cách nhiệt giúp giữ ấm đất, chống hiện tượng sương muối gây nấm bệnh trên lá và ngăn cản côn trùng, dịch hại hoạt động về đêm.

### 5. ⛈️ Chế độ Mưa lạnh ban đêm (RAINY NIGHT)
* Điều kiện: Ban đêm (18h - 05h), ánh sáng yếu/tắt hoàn toàn (< 0.55), Nhiệt độ > 23°C & Độ ẩm cực cao (>= 85%).
* Hành động phần cứng:
  * Mái che (Servo): ĐÓNG (Tắt LED trạng thái).
  * Đèn cảnh báo (RGB): Sáng màu Xanh lơ (Cyan).
  * Màn hình (LCD): Hiển thị R_NIGHT!
* Mục đích nông nghiệp: Bảo vệ khẩn cấp, ngăn chặn ngập úng cục bộ và hạn chế rủi ro cây bị hạ thân nhiệt đột ngột do nước mưa lạnh.

## 3. Cấu trúc dự án
miniature_greenhouse/
├── main.py              # File chạy chính (Menu & Chế độ tự động)
├── mock_main.py         # File chứa Chế độ Giả lập (Mô phỏng thời tiết)
├── config.py            # Cấu hình chân GPIO, ngưỡng ánh sáng (0.55 - 0.85)
├── modules/
│   ├── sensors/         # Xử lý cảm biến DHT, Light Sensor (LDR + MCP3208)
│   ├── actuators/       # Xử lý Servo, LED RGB
│   └── display/         # Xử lý màn hình LCD I2C
└── README.md            # Tài liệu dự án

## 4. Hướng dẫn vận hành
Yêu cầu tiên quyết
Hệ điều hành Raspberry Pi OS đã bật I2C (thông qua raspi-config).
Thư viện lgpio và gpiozero đã được cài đặt trên hệ thống.

### Các bước thực thi

4.1: Luôn làm bước này khi mở Terminal mới
source venv/bin/activate

4.2: Chạy chương trình
python main.py

4.3: Hệ thống sẽ hiển thị Menu lựa chọn:
      Nhấn 1: Chạy Chế độ Thực tế. Hệ thống sẽ tự động đọc cảm biến thật để điều khiển mái che và đèn.

      Nhấn 2: Chạy Chế độ Giả lập (gọi từ mock_main.py). Cho phép bạn tự chọn 1 trong 5 thời tiết để test hoạt động của LED, Servo và màn hình LCD mà không cần tác động vào cảm biến.

      (Bấm Ctrl + C bất cứ lúc nào để thoát chương trình an toàn, hệ thống sẽ tự động dọn dẹp và tắt linh kiện).

## 5. Tùy chỉnh (config.py)
Để thay đổi thông số hoạt động, hãy chỉnh sửa trực tiếp tại file config.py:

THRESHOLDS: Điều chỉnh các ngưỡng LIGHT_HIGH (mặc định 0.85) và LIGHT_LOW (mặc định 0.55) để phù hợp với độ nhạy của cảm biến quang (LDR).

GPIO: Cập nhật sơ đồ chân cắm nếu có thay đổi phần cứng (ví dụ: chuyển chân LED RGB, Servo).

LCD: Cấu hình địa chỉ I2C (thường là 0x27) và thông số kích thước màn hình.

