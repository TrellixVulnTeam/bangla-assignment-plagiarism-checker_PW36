from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import Document
from difflib import SequenceMatcher 


class PlagView(View):
    def get(self, request):
        return render(request, 'base/master.html')
    
    def post(self, request):
        
        form = Document()
        if request.method == 'POST':
            form.doc1 = request.POST['doc1']
            form.doc2 = request.POST['doc2']
            # file upload from request.FILES
            files = request.FILES.getlist('file')
            if files:
                for f in files:
                    # read the pdf file
                    with open(f.name, 'wb+') as destination:
                        for chunk in f.chunks():
                            destination.write(chunk)
                    # save the file in the database 
                    
                    form.doc1 = f.name
                    
                return HttpResponse('File uploaded.')
            else:
                return HttpResponse('No files uploaded.')
            form.save()
            similarity_ratio = SequenceMatcher(None,form.doc1,form.doc2).ratio()
            result = similarity_ratio * 100
           
        return render(request, 'base/master.html', {'hello':result, 'form':form})
    




