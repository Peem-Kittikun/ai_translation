import fitz  # PyMuPDF
from io import BytesIO
from PIL import Image
import base64
import time
import math
from collections import Counter
from PIL import Image
import cv2
import numpy as np
from config import GEMINI_API_KEY
from google import genai
from google.genai import types


class PDFExtractor:
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        print(f"Extractor initialized for: {self.pdf_path}")
        
    def read_file_md(self, file_path: str) ->str:
        """    Reads a markdown file and returns its content.

        Args:
            file_path (str): The path to the markdown file.

        Returns:
            str: The content of the markdown file.  Returns an empty string if an error occurs.
        """
        try:
            with open(file_path, "r", encoding="utf8") as file:
                data = file.read()
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return ""
        except UnicodeDecodeError as e:
            print(f"Encoding error: {e}")
            return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""
        
    def read_pdf_file(self, pdf_filepath):
        """Opens a PDF file and returns the document object."""
        return fitz.open(pdf_filepath)
                    
    
        
    def convert_page_to_base64(self, pdf_file, page:int) -> str:
        """ Convert a specific page of a PDF file to a Base64 encoded string.
        Args:
            pdf_file (fitz.Document): An OPEN PDF document object.
            page (int): The page number (0-indexed) to convert.
        Returns:
            str: The Base64 encoded string of the page image.
        Raises:
            TypeError: If the page number is not an integer.
            ValueError: If the page number is negative.
            IndexError: If the page number is out of range.
        """        
        if not isinstance(page, int):
            raise TypeError("Page number must be an integer")
    
        if page < 0:
            raise ValueError("Page number must be non-negative")
            
        # This check will now work because pdf_file is an open document
        if page >= len(pdf_file):
            raise IndexError(f"Page {page} does not exist. Document has {len(pdf_file)} pages")
                
        # Render the specific page as an image
        pdf_page = pdf_file.load_page(page)
        # Increase DPI for better quality when using with LLMs
        pix = pdf_page.get_pixmap(dpi=200) 
        
        # Convert the image to a PIL image
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        
        # Save the image to a bytes buffer
        buffer = BytesIO()
        img.save(buffer, format="PNG") # PNG is lossless and often better for text
        img_bytes = buffer.getvalue()
            
        # Encode the image bytes to Base64
        base64_pdf = base64.b64encode(img_bytes).decode('utf-8')
        
        return base64_pdf
    
    
    
    def extract_text(self,prompt_file_path,base64_pdf, temperature):
        """    Extracts text from a PDF using Vertex AI.

        Args:
            prompt_file_path (str): The path to the prompt file.
            base64_pdf (str): The base64 encoded PDF data.
            temperature (float): The temperature parameter for the model.

        Returns:
            str: The extracted text.
        
        """
        #prompt = self.read_file_md(prompt_file_path)
        client = genai.Client(api_key=GEMINI_API_KEY)

        #model = "gemini-2.5-pro-preview-06-05"
        #model = "gemini-2.0-flash"
        model = "gemini-2.0-flash-lite"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_bytes(mime_type="image/png",data=base64.b64decode(base64_pdf),),
                    types.Part.from_text(text="""extract the text from the image you recieved"""),],),]
        
        pdf_part = types.Part.from_bytes(
        mime_type="image/png",  # <-- แก้เป็น pdf
        data=base64.b64decode(base64_pdf)
        )
        text_part = types.Part.from_text(text="extract the text from the document you received")
        contents = [pdf_part, text_part]
        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="text/plain",)
        full_text =""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,):
            
            full_text += chunk.text  # Append each chunk to the full_text

        return full_text



if __name__ == "__main__":
    
    path = "./data/input/M.A.D Bootcamp - Program Journey & Course Outline.pdf"
    pdf_object = PDFExtractor(path)

    # Use a 'with' block here to manage the document's lifecycle.
    # The 'pdf_file' object will be valid inside this block and
    # automatically closed when the block is exited.
    try:
        with pdf_object.read_pdf_file(path) as pdf_file:
            print(f"PDF opened successfully. It has {len(pdf_file)} pages.")
            
            # Now we can safely call methods that use the open document
            base64_string = pdf_object.convert_page_to_base64(pdf_file, 0)
            
            print('Base64 string for page 0 generated successfully.')
            
            extracted_text = pdf_object.extract_text("",base64_string,1.0)
            print("--------------------")
            print(extracted_text)
            print("--------------------")

            # You can uncomment the line below to see a snippet of the string
            # print(f"Base64 snippet: {base64_string[:100]}...")

    except FileNotFoundError:
        print(f"Error: The file was not found at {path}")
    except IndexError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")