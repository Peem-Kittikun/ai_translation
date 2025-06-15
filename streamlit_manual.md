ยอดเยี่ยมเลยครับ! โค้ดที่คุณเขียนมาเป็นตัวอย่างการใช้งาน Streamlit ที่ดีมากสำหรับการสร้างเว็บแอปพลิเคชันง่ายๆ ครับ

ผมจะอธิบายโค้ดของคุณทีละส่วน จากนั้นจะสอนแนวคิดหลักและคำสั่งต่างๆ ของ Streamlit ให้คุณเข้าใจมากขึ้นนะครับ

---

### **ส่วนที่ 1: อธิบายโค้ด PDF Translator ของคุณ**

โค้ดนี้สร้างเว็บแอปพลิเคชันง่ายๆ สำหรับแปลไฟล์ PDF หน้าต่อหน้า เรามาดูการทำงานทีละบรรทัดกันครับ

```python
# 1. นำเข้าไลบรารีที่จำเป็น
import streamlit as st  # นี่คือพระเอกของเรา
import os
from src.pipeline_2 import TranslationPipeline 
```
- `import streamlit as st`: เป็นข้อตกลงทั่วไปในการ import ไลบรารี Streamlit และตั้งชื่อเล่นให้มันว่า `st` เพื่อให้เรียกใช้ง่าย
- `os`: ใช้สำหรับจัดการกับไฟล์และไดเรกทอรี เช่น สร้างโฟลเดอร์, รวม path ของไฟล์
- `TranslationPipeline`: นี่คือคลาสที่คุณสร้างเองจากไฟล์อื่น (`src/pipeline_2.py`) ซึ่งทำหน้าที่หลักในการแปลเอกสาร

```python
# 2. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="AI Translator", layout="centered")
st.title("📘 AI PDF Translator")
```
- `st.set_page_config(...)`: เป็นคำสั่งที่ต้องเรียกใช้เป็น **อันดับแรก** ในสคริปต์ ใช้ตั้งค่าพื้นฐานของหน้าเว็บ เช่น
    - `page_title`: ข้อความที่จะแสดงบนแท็บของเบราว์เซอร์
    - `layout`: กำหนดความกว้างของหน้าเว็บ มี `centered` (เนื้อหาอยู่ตรงกลาง, เหมาะกับแอปส่วนใหญ่) และ `wide` (เนื้อหาเต็มความกว้างจอ)
- `st.title(...)`: แสดงหัวข้อหลัก (Title) ขนาดใหญ่บนหน้าเว็บ

```python
# 3. สร้าง Widgets เพื่อรับข้อมูลจากผู้ใช้ (Input Widgets)
uploaded_file = st.file_uploader("📎 Upload your PDF file", type=["pdf"])
source_lang = st.text_input("🌐 Source Language", value="thai")
target_lang = st.text_input("🌍 Target Language", value="english")
page_num = st.number_input("📄 Page Number (starts from 1)", min_value=1, value=1)
```
- `st.file_uploader(...)`: สร้างปุ่มให้ผู้ใช้อัปโหลดไฟล์ เมื่อผู้ใช้อัปโหลดไฟล์ `uploaded_file` จะมีข้อมูลไฟล์นั้นอยู่ (ถ้ายังไม่อัปโหลดจะเป็น `None`) `type=["pdf"]` คือการจำกัดให้รับเฉพาะไฟล์ PDF
- `st.text_input(...)`: สร้างกล่องข้อความให้ผู้ใช้กรอกข้อมูล `value="thai"` คือการใส่ค่าเริ่มต้นไว้ในกล่อง
- `st.number_input(...)`: เหมือน `text_input` แต่สำหรับตัวเลขโดยเฉพาะ `min_value=1` คือการบังคับว่าค่าต้องไม่ต่ำกว่า 1

```python
# 4. สร้างปุ่มและเงื่อนไขการทำงาน
if uploaded_file and st.button("🚀 Translate"):
```
- `st.button(...)`: สร้างปุ่มขึ้นมาบนหน้าเว็บ คำสั่งนี้จะคืนค่าเป็น `True` **เฉพาะในจังหวะที่ผู้ใช้กดปุ่มนั้น** และจะคืนค่า `False` ในการรันครั้งอื่นๆ
- `if uploaded_file and ...`: เป็นเงื่อนไขสำคัญมาก หมายความว่า "ถ้ามีไฟล์อัปโหลดแล้ว **และ** ผู้ใช้กดปุ่ม 'Translate'" โค้ดที่อยู่ข้างใน `if` ถึงจะทำงาน

```python
# 5. ส่วนประมวลผล (เมื่อเงื่อนไขเป็นจริง)
    with st.spinner("🛠️ Processing... Please wait..."):
```
- `with st.spinner(...)`: เป็นคำสั่งที่ยอดเยี่ยมมาก! มันจะแสดงข้อความพร้อมกับ animation หมุนๆ ระหว่างที่โค้ดข้างใน `with` กำลังทำงานอยู่ เมื่อทำงานเสร็จ ข้อความและ animation ก็จะหายไปเอง เหมาะสำหรับงานที่ใช้เวลานาน

```python
        # เตรียม path และบันทึกไฟล์ (ส่วนนี้เป็น Python ปกติ)
        input_path = os.path.join("data", "input", uploaded_file.name)
        # ... (โค้ดจัดการไฟล์)

        # เรียกใช้ Pipeline ของคุณ
        pipeline = TranslationPipeline(...)
        pipeline.run()
```
- ส่วนนี้เป็นการทำงานเบื้องหลังที่ไม่เกี่ยวกับ Streamlit โดยตรง คือการเตรียมที่เก็บไฟล์, บันทึกไฟล์ที่ผู้ใช้อัปโหลดลงไปในเซิร์ฟเวอร์, และเรียกใช้ class `TranslationPipeline` ที่คุณเขียนไว้เพื่อทำการแปลจริงๆ

```python
# 6. แสดงผลลัพธ์และปุ่มดาวน์โหลด
        output_file_path = os.path.join(output_path, filename)
        with open(output_file_path, "rb") as f:
            st.success("✅ Translation Completed!")
            st.download_button(
                label="📥 Download Translated DOCX",
                data=f,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
```
- `st.success(...)`: แสดงกล่องข้อความสีเขียวเพื่อบอกว่าทำงานสำเร็จแล้ว
- `st.download_button(...)`: สร้างปุ่มสำหรับดาวน์โหลดไฟล์
    - `label`: ข้อความบนปุ่ม
    - `data`: **ข้อมูลของไฟล์จริงๆ** ในรูปแบบ bytes (ซึ่งได้มาจากการ `open(..., "rb")`)
    - `file_name`: ชื่อไฟล์ที่จะให้ผู้ใช้บันทึก
    - `mime`: ชนิดของไฟล์ เพื่อให้เบราว์เซอร์รู้ว่ากำลังดาวน์โหลดไฟล์ประเภทไหน (สำคัญมาก!)

---

### **ส่วนที่ 2: Streamlit ใช้งานอย่างไร? (แนวคิดหลัก)**

หัวใจสำคัญของ Streamlit คือ **"Script Reruns"**

> ทุกครั้งที่ผู้ใช้โต้ตอบกับแอป (เช่น พิมพ์ในกล่องข้อความ, เลือก Dropdown, กดปุ่ม) **Streamlit จะรันสคริปต์ Python ของคุณใหม่ทั้งหมดตั้งแต่ต้นจนจบ!**

**ตัวอย่างจากโค้ดของคุณ:**
1.  **เปิดแอปครั้งแรก:** สคริปต์รัน `uploaded_file` เป็น `None` และ `st.button` เป็น `False` ดังนั้นโค้ดใน `if` ไม่ทำงาน แอปจะแสดงแค่ Title และ widget ต่างๆ รอผู้ใช้
2.  **ผู้ใช้อัปโหลด PDF:** แอปจะ **รันใหม่!** ครั้งนี้ `uploaded_file` จะมีข้อมูลไฟล์อยู่ แต่ `st.button` ยังเป็น `False` โค้ดใน `if` ก็ยังไม่ทำงาน
3.  **ผู้ใช้กดปุ่ม "Translate":** แอปจะ **รันใหม่อีกครั้ง!** ครั้งนี้ `uploaded_file` มีข้อมูล **และ** `st.button` คืนค่า `True`! ทำให้เงื่อนไขเป็นจริง โค้ดใน `if` จึงทำงาน เกิดการแปลไฟล์ และแสดงปุ่มดาวน์โหลด

การเข้าใจแนวคิด "Script Reruns" นี้จะช่วยให้คุณออกแบบแอปได้ดีขึ้นมากครับ

---

### **ส่วนที่ 3: รวมคำสั่ง Streamlit ที่ใช้บ่อย**

Streamlit มีคำสั่งมากมายที่แบ่งเป็นหมวดหมู่ได้ดังนี้ครับ

#### **1. การแสดงข้อความ (Display Text)**
- `st.title("หัวข้อใหญ่สุด")`
- `st.header("หัวข้อรอง")`
- `st.subheader("หัวข้อย่อย")`
- `st.write("ข้อความทั่วไป", variable, dataframe)`: เป็นคำสั่งอเนกประสงค์ แสดงได้ทั้งข้อความ, ตัวแปร, หรือแม้แต่ตาราง
- `st.markdown("รองรับ *Markdown* **เหมือนใน** [GitHub](url))"`: สำหรับคนที่ถนัดเขียน Markdown
- `st.code("print('Hello World')", language="python")`: แสดงโค้ดสวยๆ

#### **2. การแสดงข้อมูล (Display Data)**
- `st.dataframe(df)`: แสดงตารางข้อมูลจาก Pandas DataFrame แบบ interactive (เรียงข้อมูล, ค้นหาได้)
- `st.table(df)`: แสดงตารางแบบธรรมดา (Static)
- `st.metric(label="อุณหภูมิ", value="25 °C", delta="1.5 °C")`: แสดงค่าตัวเลขที่สำคัญ พร้อมค่าความเปลี่ยนแปลง (delta)
- `st.json({"name": "John", "age": 30})`: แสดงข้อมูล JSON

#### **3. การแสดงสื่อ (Display Media)**
- `st.image("path/to/image.jpg", caption="คำอธิบายภาพ")`
- `st.audio("path/to/audio.mp3")`
- `st.video("path/to/video.mp4")`

#### **4. การรับข้อมูลจากผู้ใช้ (Input Widgets)**
- `st.button("Click me")`: ปุ่มกด
- `st.checkbox("ฉันยอมรับเงื่อนไข")`: กล่องติ๊กถูก
- `st.radio("เลือกข้อเดียว", ["A", "B", "C"])`: ตัวเลือกแบบเลือกได้ข้อเดียว
- `st.selectbox("เลือกจังหวัด", ["กทม", "เชียงใหม่", "ภูเก็ต"])`: Dropdown list
- `st.multiselect("เลือกหลายจังหวัด", ["กทม", "เชียงใหม่", "ภูเก็ต"])`: Dropdown แบบเลือกได้หลายข้อ
- `st.slider("เลือกช่วงอายุ", 0, 100, 25)`: แถบเลื่อน (min, max, default)
- `st.text_input("ชื่อของคุณ")` / `st.text_area("ความคิดเห็น")`
- `st.number_input("จำนวน")`
- `st.date_input("วันเกิด")` / `st.time_input("เวลานัดหมาย")`
- `st.file_uploader("อัปโหลดไฟล์")`
- `st.color_picker("เลือกสีที่ชอบ")`

#### **5. การจัด Layout และ Containers**
- `st.sidebar`: คำสั่งที่ใช้กับ `st.sidebar` จะไปปรากฏที่แถบด้านข้างแทน เช่น `st.sidebar.header("เมนู")`
- `col1, col2, col3 = st.columns(3)`: แบ่งหน้าจอเป็นคอลัมน์
  ```python
  col1, col2 = st.columns(2)
  with col1:
      st.header("ฝั่งซ้าย")
      st.image("image1.jpg")
  with col2:
      st.header("ฝั่งขวา")
      st.image("image2.jpg")
  ```
- `with st.expander("คลิกเพื่อดูรายละเอียดเพิ่มเติม"):`: สร้างกล่องที่พับ/ขยายได้
- `st.container()`: สร้างกล่องเปล่าๆ สำหรับจัดกลุ่ม element

#### **6. การแสดงสถานะ (Status Elements)**
- `st.progress(percentage)`: แสดงแถบความคืบหน้า
- `st.spinner("กำลังโหลด...")`: แสดง animation หมุนๆ ขณะรอ
- `st.balloons()` / `st.snow()`: แสดง animation สนุกๆ เพื่อฉลองความสำเร็จ
- `st.error("เกิดข้อผิดพลาด!")`
- `st.warning("คำเตือน")`
- `st.info("ข้อมูลเพิ่มเติม")`
- `st.success("สำเร็จ!")`

### **วิธีเริ่มใช้งานและรันแอป**

1.  **ติดตั้ง Streamlit:**
    ```bash
    pip install streamlit
    ```

2.  **บันทึกโค้ด:** บันทึกโค้ดของคุณเป็นไฟล์ `.py` เช่น `app.py`

3.  **รันแอปผ่าน Terminal:**
    ```bash
    streamlit run app.py
    ```

หลังจากรันคำสั่งนี้ Streamlit จะเปิดเบราว์เซอร์ขึ้นมาแสดงเว็บแอปของคุณโดยอัตโนมัติ และทุกครั้งที่คุณแก้ไขและบันทึกไฟล์ `app.py` เว็บแอปในเบราว์เซอร์ก็จะอัปเดตตามทันที!

หวังว่าคำอธิบายนี้จะช่วยให้คุณเข้าใจ Streamlit และนำไปต่อยอดสร้างโปรเจกต์เจ๋งๆ ได้มากขึ้นนะครับ! ถ้ามีคำถามเพิ่มเติม ถามได้เลยครับ