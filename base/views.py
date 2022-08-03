from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import Document
from difflib import SequenceMatcher 
from tempfile import TemporaryDirectory
from pathlib import Path
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
class PlagView(View):
    def get(self, request):
        return render(request, 'base/master.html')
    
    def post(self, request):
        out_directory = Path("~").expanduser()
        form = Document()
        if request.method == 'POST':
            form.doc1 = request.POST['doc1']
            form.doc2 = request.POST['doc2']
            # file upload from request.FILES
            for pdf in request.FILES.getlist("files"):
            # return HttpResponse(files)
            
                if pdf:

                    out_directory = Path("~").expanduser()
                    image_file_list = []
                    text_file = out_directory / Path("out_text.txt")
                    all_text = ''
                    key = 0;
                    # return HttpResponse(pytesseract.get_languages(config=''))
                    with TemporaryDirectory() as tempdir:
                        pdf_pages = convert_from_bytes(pdf.read())
                        for page_enumeration, page in enumerate(pdf_pages, start=1):
                            filename = f"{tempdir}\page_{page_enumeration:03}.jpg"
                            page.save(filename, "JPEG")
                            image_file_list.append(filename)
                        else:
                            for image_file in image_file_list:
                                text = pytesseract.image_to_string(Image.open(image_file),lang="ben")
                                all_text += text
                    tokenizeText = self.tokenize(all_text)
                    # split text into sentences and tokenize each sentence coma separated 
                    # tokenizeText = [tokenizeText[0].split(',') ]
                    return HttpResponse(tokenizeText)
                    return HttpResponse(tokenizeText)
                else:
                    return HttpResponse('No files uploaded.')
            # form.save()
            # similarity_ratio = SequenceMatcher(None,form.doc1,form.doc2).ratio()
            # result = similarity_ratio * 100
           
        return render(request, 'base/master.html', {'hello':result, 'form':form})
    

    def get_similarity_ratio(self, doc1, doc2):
        return SequenceMatcher(None, doc1, doc2).ratio() * 100
    
    def tokenize(self, doc):
        return sent_tokenize(doc)


