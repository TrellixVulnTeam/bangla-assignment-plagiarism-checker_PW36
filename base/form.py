from django import forms
from .models import Document

class Document(forms.Form):
    doc1 = forms.CharField(widget=forms.Textarea)
    doc2 = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        
        model = Document
        fields = ['doc1', 'doc2']
        
        
        