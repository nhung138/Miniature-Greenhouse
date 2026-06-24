import board
import adafruit_dht
from config import CONFIG

class DHTManager:  
    def __init__(self):
        # Chân GPIO 17
        self.dht = adafruit_dht.DHT11(board.D17)
        
    def read(self):
        try:
            return self.dht.temperature, self.dht.humidity
        except:
            return None, None