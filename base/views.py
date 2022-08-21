from array import array
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import Document
import nltk
nltk.download('punkt')
from .pdf_convertier import PdfConvertre
from .plagarism_checker import PlagiarismChecker
class PlagView(View):
    def get(self, request):
        return render(request, 'base/master.html')
    
    def post(self, request):
        # out_directory = Path("~").expanduser()
        
        if request.method == 'POST':
            form = Document()
            pdf_text = PdfConvertre.converter(request.FILES.getlist("files"))
            
            # result = PlagiarismChecker.levenshtein(pdf_text[0], pdf_text[1])
            return HttpResponse(pdf_text)
            # form.save()
            # similarity_ratio = SequenceMatcher(None,form.doc1,form.doc2).ratio()
            # result = similarity_ratio * 100
           
        # return render(request, 'base/master.html', {'hello':result, 'form':form})
