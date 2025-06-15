import streamlit as st
import os
from src.pipeline_2 import TranslationPipeline  # เปลี่ยนตามชื่อไฟล์คุณ

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Translator", layout="centered")
st.title("📘 AI PDF Translator")

# อัปโหลด PDF
uploaded_file = st.file_uploader("📎 Upload your PDF file", type=["pdf"])

# เลือกภาษาต้นทางและเป้าหมาย
source_lang = st.text_input("🌐 Source Language", value="thai")
target_lang = st.text_input("🌍 Target Language", value="english")

# เลือกหน้าที่ต้องการแปล
page_num = st.number_input("📄 Page Number (starts from 1)", min_value=1, value=1)

# กดปุ่มแปล
if uploaded_file and st.button("🚀 Translate"):
    with st.spinner("🛠️ Processing... Please wait..."):
        # เตรียม path
        input_path = os.path.join("data", "input", uploaded_file.name)
        output_path = os.path.join("data", "output")
        os.makedirs(output_path, exist_ok=True)
        filename = uploaded_file.name.replace(".pdf", ".docx")

        # บันทึกไฟล์ PDF ที่อัปโหลดไว้
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # เรียกใช้ TranslationPipeline
        pipeline = TranslationPipeline(
            input_pdf_path=input_path,
            source_lang=source_lang,
            target_lang=target_lang,
            page_num=page_num,
            output_docx_path=output_path,
            filename=filename
        )
        pipeline.run()

        # แสดงผลลัพธ์ และให้ดาวน์โหลด
        output_file_path = os.path.join(output_path, filename)
        with open(output_file_path, "rb") as f:
            st.success("✅ Translation Completed!")
            st.download_button(
                label="📥 Download Translated DOCX",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
