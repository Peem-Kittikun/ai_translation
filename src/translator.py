import base64
import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY

class GeminiTranslator:
    def __init__(self,original_text,source_lang,target_lang):
        
        self.source_lang=source_lang
        self.target_lang=target_lang
        self.original_text=original_text
        print("Translator initialized.")




    def translate(self):
        client = genai.Client(api_key=GEMINI_API_KEY)

        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"""Your task is to translate the text below from {self.source_lang} to {self.target_lang} language
                                         text: {self.original_text}"""),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            temperature=0,
            response_mime_type="text/plain",
        )
        full_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,):
            
            full_text += chunk.text
            
        return full_text

if __name__ == "__main__":
    text = """Here's the text extracted from the document:
M.A.D Bootcamp - Program Journey & Course Outline
M.A.D Bootcamp คืออะไร ?
KBTG เปิดโอกาสให้บุคคลทั่วไปที่สนใจ พัฒนาทักษะด้าน Al เข้าร่วมอบรมแบบ e-Learning ผ่านระบบ
TU NEXT และกิจกรรมอีกมากมายจากทางโครงการฯ
โดยหลักสูตรรวบรวมเนื้อหา 3 ด้าน ได้แก่
1. Predictive Al
2. Large Language Model (LLM)
3. Human Al Interaction
เหมาะสำหรับผู้ที่ต้องการเข้าใจ AI ตั้งแต่ความรู้ขั้นพื้นฐาน ไปจนถึงการพัฒนา AI ด้วยตนเอง
กำหนดการณ์การรับสมัคร
ลำดับ รายการ
วันที่
"""
    content = GeminiTranslator(text,'thai','english')
    #print(content.original_text)
    print(content.source_lang)
    print(content.target_lang)
    translated_text = content.translate()
    print(translated_text)
    print(content.__dict__)