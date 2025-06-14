import os
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env เข้าสู่ environment variables
load_dotenv()

# อ่านค่าจาก environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#print(GEMINI_API_KEY)