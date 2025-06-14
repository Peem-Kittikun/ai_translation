from pdf_handler import PDFExtractor
from translator import GeminiTranslator
from validator import AIValidator
from config import GEMINI_API_KEY



class TranslationPipeline:
    def __init__(self,input_pdf_path,source_lang,target_lang,page_num,output_docx_path):
        self.input_pdf_path=input_pdf_path
        self.source_lang=source_lang
        self.target_lang=target_lang
        self.page_num =page_num
        self.output_docx_path=output_docx_path
    

    def run(self):
        print("--- Starting Translation Pipeline ---")
        
        pdf_handler = PDFExtractor(self.input_pdf_path)
        pdf_file = pdf_handler.read_pdf_file(self.input_pdf_path)
        base64_data = pdf_handler.convert_page_to_base64(pdf_file,self.page_num)
        extract_text = pdf_handler.extract_text('',base64_data,1)
        
        __translator = GeminiTranslator(extract_text,self.source_lang,self.target_lang)
        translated_text = __translator.translate()
        
        _validator = AIValidator(extract_text,translated_text,self.source_lang,self.target_lang)
        validate_result =_validator.validate_translation()
        
        print('------translated-----')
        print(translated_text)
        print('------translated end-----/n')
        
        print('------validate start-----')
        print(validate_result)
        print("\n--- Pipeline Finished Successfully ---")

if __name__ == "__main__":
    INPUT_PDF = "path/to/your/document.pdf"
    OUTPUT_DOCX = "path/to/your/translated_document.docx"
    source_lang = 'thai'
    target_lang = 'english'
    path = "./data/input/M.A.D Bootcamp - Program Journey & Course Outline.pdf"
    # สร้างและรัน Pipeline
    pipeline = TranslationPipeline(path,source_lang,target_lang,2,'')
    pipeline.run()