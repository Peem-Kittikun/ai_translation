import os
from dotenv import load_dotenv
from src.pipeline import TranslationPipeline

# โหลดค่าจากไฟล์ .env เข้าสู่ environment variables
load_dotenv()

def main():
    # ดึง API Key จาก environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in the .env file.")
        return

    # กำหนดพาธของไฟล์
    input_file = "data/input/your_document.pdf"
    output_file = "data/output/translated_document.docx"

    # สร้างและรัน pipeline
    pipeline = TranslationPipeline(api_key=api_key)
    pipeline.run(input_pdf_path=input_file, output_docx_path=output_file)

if __name__ == "__main__":
    main()