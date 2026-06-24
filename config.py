import os
from dotenv import load_dotenv

# 1. Tự tìm và nạp file .env ngay khi file này được import
base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)

# 2. Sau khi đã load, mới định nghĩa CONFIG
CONFIG = {
    "GPIO": {
        "DHT": 17,
        "SERVO": 18,
        "SERVO_LED": 12,
        "RGB": {"R": 26, "G": 19, "B": 13}
    },
    "THRESHOLDS": {
        "TEMP_HIGH": 35.0,
        "LIGHT_HIGH": 0.80,
        "LIGHT_LOW": 0.60
    },
    "WEATHER": {
        "HUMIDITY_RAIN_THRESHOLD": 90, # Độ ẩm >= 85% coi là mưa
        "LIGHT_SUNNY_THRESHOLD": 0.70   # Ánh sáng >= 0.85 coi là nắng
    },
    "LCD": {
        "ADDRESS": 0x27,
        "COLS": 16,
        "ROWS": 2
    },
    "FAILSAFE": {
        "MAX_ERRORS": 3,
        "LOCK_MODE_SERVO": False
    },
    "API_KEYS": {
        "GEMINI": os.getenv("GEMINI_API_KEY"),
        "LINE": os.getenv("LINE_NOTIFY_TOKEN"),
        "OPENWEATHER": os.getenv("OPENWEATHER_API_KEY")
    }
}