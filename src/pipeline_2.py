# from pdf_handler import PDFExtractor
# from translator import GeminiTranslator
# from validator import AIValidator
# from writer import DocxWriter
# from config import GEMINI_API_KEY
from src.pdf_handler import PDFExtractor
from src.translator import GeminiTranslator
from src.validator import AIValidator
from src.writer import DocxWriter
from src.config import GEMINI_API_KEY
import psycopg2


class TranslationPipeline:
    
    
    def __init__(self,input_pdf_path,source_lang,target_lang,page_num,output_docx_path,filename):
        self.input_pdf_path=input_pdf_path
        self.source_lang=source_lang
        self.target_lang=target_lang
        self.page_num =page_num
        self.output_docx_path=output_docx_path
        self.pdf_handler = PDFExtractor()
        self.__translator = GeminiTranslator()
        self.filename=filename
        self.docxwriter = DocxWriter(self.output_docx_path,self.filename)
    

    def run(self):
        print("--- Starting Translation Pipeline ---")
        
        
        #pdf_file = self.pdf_handler.read_pdf_file(self.input_pdf_path)
        #base64_data = self.pdf_handler.convert_page_to_base64(pdf_file,self.page_num)
        #prompt_file_path,input_pdf_path,page_num
        
        extract_text = self.pdf_handler.extract_text('',self.input_pdf_path,self.page_num,temperature=1)
        
        
        translated_text = self.__translator.translate(extract_text,self.source_lang,self.target_lang)
        
        _validator = AIValidator(extract_text,translated_text,self.source_lang,self.target_lang)
        validate_result =_validator.validate_translation()
        
        print('------translated-----')
        print(translated_text)
        print('------translated end-----/n')
        
        print('------validate start-----')
        print(validate_result)
        print('------validate stop-----')
        
        
        print('------Save file to docx-----')
        save_text = f"{translated_text}\n{validate_result}"
        savefile = self.docxwriter.write_to_docx(save_text)
        
        # Save to database
        self.save_to_db(self.filename, extract_text, translated_text)
        print("\n--- Pipeline Finished Successfully ---")
        
    def save_to_db(self,filename, src_text, translated_text):
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="1234",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS public.translated_log (
                    id SERIAL PRIMARY KEY,
                    filename TEXT,
                    src_text TEXT,
                    translated_text TEXT
                )
            """)
            cur.execute(
                "INSERT INTO public.translated_log (filename, src_text, translated_text) VALUES (%s, %s, %s)",
                (filename, src_text, translated_text)
            )
            conn.commit()
            cur.close()
            conn.close()

if __name__ == "__main__":
    filename='testt3'
    INPUT_PDF = "./data/input/M.A.D Bootcamp - Program Journey & Course Outline.pdf"
    OUTPUT_DOCX = "./data/output"
    source_lang = 'thai'
    target_lang = 'english'
    path = "./data/input/M.A.D Bootcamp - Program Journey & Course Outline.pdf"
    # สร้างและรัน Pipeline
    pipeline = TranslationPipeline(path,source_lang,target_lang,4,OUTPUT_DOCX,filename)
    pipeline.run()