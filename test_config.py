import os
from dotenv import load_dotenv, find_dotenv

# Tìm xem file .env có thực sự tồn tại không
dotenv_path = find_dotenv() 
print(f"File .env được tìm thấy tại: {dotenv_path}")

# Thử load và in ra kết quả của hàm load (True/False)
is_loaded = load_dotenv(dotenv_path)
print(f"Trạng thái load file .env: {is_loaded}")

# Kiểm tra xem key có tồn tại trong môi trường không
key_value = os.getenv("GEMINI_API_KEY")
print(f"Giá trị thực tế của biến GEMINI_API_KEY trong hệ thống: {key_value}")

# Cuối cùng là in CONFIG
from config import CONFIG
print(f"Giá trị CONFIG['API_KEYS']['GEMINI']: {CONFIG['API_KEYS']['GEMINI']}")