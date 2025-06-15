import os
from docx import Document

class DocxWriter:
    def __init__(self, output_folder,filename):
        self.output_folder = output_folder
        self.filename = filename

    def write_to_docx(self, translated_text):
        # ตรวจสอบว่ามี .docx ต่อท้ายหรือยัง
        if not self.filename.lower().endswith('.docx'):
            self.filename += '.docx'

        # สร้าง path รวม
        full_path = os.path.join(self.output_folder, self.filename)

        # เขียนไฟล์
        document = Document()
        document.add_paragraph(translated_text)
        document.save(full_path)

        print(f"✅ Successfully wrote to: {full_path}")
        
        
        
if __name__ == "__main__":
    text = """**M.A.D Bootcamp - Program Journey & Course Outline**

**Course Overview**

1.  Predictive AI
    *   Introduction to Predictive AI
    *   Real Use Cases
    *   Fundamental of Data Analysis

2.  Large Language Model (LLM)
    *   Introduction to LLM
    *   Get to Know LLM API
    *   Prompt Engineering Basics
    *   LLM API for Beginners
    *   Leveraging LLM API

3.  Human AI Interaction
    *   Principle of Human AI Interaction
    *   Introduction to HCI
    *   Ideation & Brainstorming
    *   Interface Design and Evaluation
    *   Human & AI
    *   Content and Conversational AI
    *   Augmented Intelligence
    *   Future Trends and Challenges
    *   Apply Human & AI
    *   Generating an image using stable diffusion
    *   Retrieval-Augmented Generation (RAG) with LangChain

**Course Outline**

**Module 1: Predictive AI**

Students will encounter methods for studying data, delving into the skills of building AI models to predict the future and confidently use data in decision-making. This involves using advanced mathematical, statistical, and Machine Learning techniques combined in data analysis.

Total hours in this Module: 15 hours

**Predictive AI - Course Outline**

Lesson 1: Introduction to Predictive AI
    *   What is AI?
    *   Introduction to Data

Lesson 2: Real Use Cases
    *   Example of predictive AI capabilities
    *   Overview of designing and building AI systems through real-world use cases
    *   Workflow for building predictive AI

Lesson 3: Fundamental of Data Analysis
    *   Introduction to data analysis
    *   Data analysis pipeline and exploratory data analysis (EDA)
    *   Data Visualization
    *   Introduction to google colab & Data Visualisation lab

Lesson 4: Principle of Machine Learning
    *   Introduction to Machine Learning
    *   Major of machine learning models (Supervised learning, Unsupervised learning)
    *   Overfitting and Underfitting in supervised learning problem
    *   Train-test-validation split
    *   Example of real use case in supervised learning problem

KBTG Kampus ClassNest

Page 3"""
    folder = "./data/output"
    filename = "translated_page1"

    # สร้างโฟลเดอร์ถ้ายังไม่มี
    os.makedirs(folder, exist_ok=True)

    writer = DocxWriter(folder)
    writer.write_to_docx(text, filename)

