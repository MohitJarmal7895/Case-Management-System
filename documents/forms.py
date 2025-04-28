from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'description', 'case']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }