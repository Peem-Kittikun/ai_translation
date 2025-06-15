import base64
import os
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY

class AIValidator:
    def __init__(self,original_text,translated_text,source_lang,target_lang):
        self.source_lang=source_lang
        self.target_lang=target_lang
        self.original_text=original_text
        self.translated_text=translated_text
        # genai.configure(api_key=api_key)
        # self.model = genai.GenerativeModel('gemini-pro')
        print("Validator initialized.")
    
    def validate_translation(self):
        print("Validating translation...")
        client = genai.Client(api_key=GEMINI_API_KEY)

        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"""You are a professional in translate the text below from {self.source_lang} to {self.target_lang} language
                                         your task is to validate the translated text here : {self.translated_text} , original text is {self.original_text}
                                         Give the score:1-10 point and , comment: """),
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
    
if __name__ =="__main__":
    
    original_text="""Here's the text extracted from the document:
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
วันที่"""
    translated_text="""**M.A.D Bootcamp - Program Journey & Course Outline**

**What is M.A.D Bootcamp?**

KBTG offers an opportunity for the general public interested in developing AI skills to participate in e-Learning training through the TU NEXT system and various activities from the project.

The curriculum covers content in 3 areas:

1.  Predictive AI
2.  Large Language Model (LLM)
3.  Human AI Interaction

Suitable for those who want to understand AI from basic knowledge to developing AI on their own.

**Application Schedule**

| No. | Item | Date |
|---|---|---|"""
    validatation = AIValidator(original_text,translated_text,'thai','english')
    
    validation_score = validatation.validate_translation()
    print(validation_score)