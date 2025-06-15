import os
from src.pipeline_2 import TranslationPipeline  # <-- เปลี่ยนเป็น path ที่คุณใช้จริง ถ้าอยู่ใน src
# หรือหาก class อยู่ในไฟล์เดียวกันกับ main.py ให้ลบบรรทัดนี้

def main():
    # กำหนดค่าต่างๆ
    filename = 'testt3.docx'
    input_pdf_path = "./data/input/M.A.D Bootcamp - Program Journey & Course Outline.pdf"
    output_docx_path = "./data/output"
    source_lang = 'thai'
    target_lang = 'english'
    page_num = 4

    # ตรวจสอบ path
    if not os.path.exists(input_pdf_path):
        raise FileNotFoundError(f"ไม่พบไฟล์ PDF: {input_pdf_path}")

    os.makedirs(output_docx_path, exist_ok=True)

    # เรียกใช้ Pipeline
    pipeline = TranslationPipeline(
        input_pdf_path=input_pdf_path,
        source_lang=source_lang,
        target_lang=target_lang,
        page_num=page_num,
        output_docx_path=output_docx_path,
        filename=filename
    )
    pipeline.run()

if __name__ == "__main__":
    main()
