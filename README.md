Miniature Greenhouse (Nhà kính Mini)
Hệ thống nhà kính thông minh sử dụng Raspberry Pi, tích hợp cảm biến môi trường, cơ chế tư vấn chăm sóc cây trồng thông minh (Offline AI) và giao diện giám sát thời gian thực.

🏗️ Giới thiệu hệ thống
Hệ thống tự động giám sát môi trường (nhiệt độ, độ ẩm, ánh sáng) và điều khiển cơ cấu chấp hành (mái che servo) dựa trên các chế độ thời tiết thực tế. Điểm đặc biệt của phiên bản này là hệ thống tự đưa ra lời khuyên chuyên gia dựa trên dữ liệu cảm biến mà không cần kết nối internet hay tiêu tốn lượt gọi API.

⚙️ Điều kiện hoạt động và Logic xử lý
Hệ thống vận hành dựa trên bộ lọc điều kiện chặt chẽ, phân loại môi trường thành 5 chế độ chính để đưa ra quyết định đóng/mở mái che tự động:

SUNNY (Nắng): Ánh sáng cao (> 0.6), Độ ẩm < 80%.

Hành động: Mở mái che để cây nhận đủ ánh sáng quang hợp.

CLOUDY (Nhiều mây): Ánh sáng trung bình (0.3 - 0.6), Độ ẩm < 80%.

Hành động: Mở mái che, duy trì theo dõi nhiệt độ để đảm bảo cây không bị sốc nhiệt.

R_DAY (Ngày mưa): Ánh sáng ban ngày (> 0.3) nhưng Độ ẩm > 80%.

Hành động: Tự động đóng mái che để ngăn nước mưa làm ngập úng hoặc dập nát lá cây.

NIGHT (Đêm): Ánh sáng yếu (< 0.3), Độ ẩm < 80%.

Hành động: Giữ hệ thống ổn định, cây bước vào trạng thái nghỉ ngơi.

R_NIGHT (Đêm mưa): Ánh sáng yếu (< 0.3) kết hợp Độ ẩm > 80%.

Hành động: Đóng mái che tuyệt đối để bảo vệ cây khỏi mưa đêm.

Lưu ý: Các ngưỡng thông số này được cấu hình linh hoạt trong main.py để phù hợp với từng giống cây trồng cụ thể.

🧠 Cơ chế tư vấn thông minh (Offline)
Thay vì gọi API bên thứ ba, hệ thống sử dụng module ai_consultant.py được tối ưu hóa:

Logic hoạt động: Dựa trên trạng thái (current_mode), hệ thống truy xuất vào kho dữ liệu lời khuyên được định nghĩa sẵn.

Song ngữ: Mỗi lời khuyên được thiết kế chuẩn song ngữ Nhật - Việt, mang phong cách vui tươi, truyền cảm hứng.

Độ trễ: Phản hồi gần như tức thì (~0.1s), đảm bảo giao diện luôn cập nhật trạng thái mới nhất ngay khi cảm biến thay đổi.

Độ ổn định: Không lỗi 429 (Quota Exceeded), không phụ thuộc mạng, an toàn tuyệt đối cho buổi thuyết trình.

🛠️ Hướng dẫn cài đặt & Chạy hệ thống
1. Cấu trúc logic điều khiển
main.py: Đọc cảm biến DHT22, tính toán chế độ (SUNNY, CLOUDY, R_DAY, NIGHT), gửi dữ liệu về API.

api.py: Nhận trạng thái từ main.py, gọi hàm get_pro_advice từ ai_consultant.py để lấy lời khuyên.

ai_consultant.py: Chứa kho dữ liệu lời khuyên (Hardcoded Advice).

2. Lệnh khởi động (Sau khi bật máy)
Chỉ cần mở Terminal và chạy lệnh sau để khôi phục toàn bộ tiến trình:

Bash
pm2 resurrect
Lưu ý: Nếu cần khởi tạo mới hoàn toàn:

Bash
pm2 delete all
pm2 start api.py --name "api-backend" --interpreter .venv/bin/python
pm2 start main.py --name "hardware-main" --interpreter .venv/bin/python
pm2 start npm --name "web-frontend" --cwd greenhouse-dashboard -- start
pm2 save
⚙️ Quản lý tiến trình với PM2
Kiểm tra trạng thái: pm2 status

Xem logs trực tiếp (rất hữu ích để demo): ```bash
pm2 logs hardware-main --lines 20

Lưu cấu hình khởi động: Luôn nhớ chạy pm2 save sau khi thay đổi bất kỳ tiến trình nào.