import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Sử dụng connection string từ biến môi trường
    MONGO_URI = os.getenv('MONGO_URI')
