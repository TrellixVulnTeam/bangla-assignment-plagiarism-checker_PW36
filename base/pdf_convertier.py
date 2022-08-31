from tempfile import TemporaryDirectory
from pathlib import Path
from django.core.files import File
from nltk.tokenize import sent_tokenize
import nltk as nl
import pytesseract
from pdf2image import convert_from_bytes
from .image_converter import ImageConverter
from PIL import Image
class PdfConvertre:
    
    def converter (pdf) -> None:
        
        image_converter = ImageConverter()
        if pdf:
            image_file_list = []
            all_text = ''
            with TemporaryDirectory() as tempdir:
                pdf_pages = convert_from_bytes(pdf.read())
                for page_enumeration, page in enumerate(pdf_pages, start=1):
                    filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
                    page.save(filename, "JPEG")
                    image_file_list.append(filename)
                else:
                    all_text = image_converter.convert(image_file_list) # convert this all images using ocr
            return all_text.split("।")
        else:
            return 'this is not a pdf'
