from array import array
from ast import And
from curses.ascii import HT
from difflib import SequenceMatcher
from pydoc import doc
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

            doc1 = request.POST.get('doc1', False)
            doc2 = request.POST.get('doc2', False)
            if doc1 and doc2:
                pdfPlag = PlagiarismChecker()
                arrayOfResult = pdfPlag.plugCheckFromTextArray(pdfPlag.textSplit(doc1), pdfPlag.textSplit(doc2))
                dic = {'text':arrayOfResult[0], 'percen': arrayOfResult[1]}
                return render(request, 'base/master.html', {'results':dic, 'tab':tab, 'form':{doc1:doc1, doc2:doc2}})

            multifiles = request.FILES.getlist('files')
            if multifiles and len(multifiles) > 2:
                tab = 'multi'
                files = request.FILES.getlist('files')
                multi_file_instence = MultiFile(files)
                res = multi_file_instence.multifilePlugCheck()
                return render(request, 'base/master.html', {'results':res, 'tab':tab})

            # 1-2, 1-3, 1-8, 2-3, 2-8, 3-8
            file1 = request.FILES['file1']
            file2 = request.FILES['file2']
            if len(file1) > 0 and len(file2) > 0:
                tab = 'two_pdf'
                pdf_text1 = PdfConvertre.converter(request.FILES["file1"])
                pdf_text2 = PdfConvertre.converter(request.FILES["file2"])
                pdfPlag = PlagiarismChecker()
                similerText = pdfPlag.santenceSimilarity(pdf_text1, pdf_text2)
                percentage = pdfPlag.percentageOfText(pdf_text1, pdf_text2)
                dic = {'between':file1.name + " " + file2.name,'text':similerText, 'percen': percentage}
                return render(request, 'base/master.html', {'results':dic, 'tab':tab})

            singleFile = request.FILES('singleFile')
            multiFile = request.FILES.getlist('multiFile')
            if singleFile and len(multiFile) > 0:
                tab = 'one_to_many' 
                single_pdf_text = PdfConvertre.converter(singleFile)
                mulple_file_instance = MultiFile(multiFile)
                plag_result = mulple_file_instance.single_file_to_multifile_plug_check(single_pdf_text, singleFile.name, multi_file_instence.convert_pdf_to_text_from_all_files()) 
                return render(request, 'base/master.html', {'results':dic, 'tab':tab})



            

        # return render(request, 'base/master.html', {'hello':result, 'form':form})
