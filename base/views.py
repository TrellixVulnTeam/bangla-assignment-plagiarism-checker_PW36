from array import array
from ast import And
from curses.ascii import HT
from difflib import SequenceMatcher
from unittest import result
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from base.multi_file_to_array_text import MultiFile
from .models import Document
import nltk
nltk.download('punkt')
from .pdf_convertier import PdfConvertre
from .plagarism_checker import PlagiarismChecker
from .image_converter import ImageConverter
class PlagView(View):
    def get(self, request):

        return render(request, 'base/master.html',{'tab': 'home'})
    
    def post(self, request):
        # out_directory = Path("~").expanduser()
        
        if request.method == 'POST':
            tab = "home"
            multifiles = request.FILES.getlist('files')
            if multifiles and len(multifiles) > 2:
                tab = 'multi'
                files = request.FILES.getlist('files')
                multi_file_instence = MultiFile(files)
                res = multi_file_instence.multifilePlugCheck()
                return render(request, 'base/master.html', {'results':res, 'tab':tab})

            # 1-2, 1-3, 1-8, 2-3, 2-8, 3-8
            file1 = request.FILES["file1"]
            file2 = request.FILES["file2"]
            if file1 and file2:
                tab = 'two_pdf'
                pdf_text1 = PdfConvertre.converter(file1)
                pdf_text2 = PdfConvertre.converter(file2)
                pdfPlag = PlagiarismChecker()
                similerText = pdfPlag.santenceSimilarity(pdf_text1, pdf_text2)
                percentage = pdfPlag.percentageOfText(pdf_text1, pdf_text2)
                dic = {'between':file1.name + " " + file2.name,'text':similerText, 'percen': percentage}
                return render(request, 'base/master.html', {'results':dic, 'tab':tab})

            # if request.doc1 and request.doc2:

            

        # return render(request, 'base/master.html', {'hello':result, 'form':form})
