from tempfile import TemporaryDirectory
from pathlib import Path
from django.core.files import File
from nltk.tokenize import sent_tokenize
import nltk as nl
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
from .plagarism_checker import PlagiarismChecker
class PdfConvertre:
    
    def converter (pdfs) -> None:
        array_of_all_text = []
        for pdf in pdfs :
            pdf_name = pdf.name
            
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
                        for image_file in image_file_list:
                            text = pytesseract.image_to_string(Image.open(image_file),lang="ben")
                            text = text.replace('\n', ' ')
                            all_text += text
                
                singlePdfText = all_text.split("।")
                    # all_array_taxt = {pdf_name:all_text} 
                    # array_of_all_text.append(all_array_taxt)
                pl = PlagiarismChecker()
                
                # Removing stopwords
                # dbtokens = [i for i in singlePdfText if i not in pl.bangla_stopwords]
                array_of_all_text.append(singlePdfText)
            else:
                return 'this is not a pdf'
        
        return array_of_all_text