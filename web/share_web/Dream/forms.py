from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file', )

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')