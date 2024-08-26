from django import forms
from .models import Certificate, Microblog

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['name', 'issuer', 'date_issued', 'image']
        widgets = {
            'date_issued': forms.DateInput(attrs={'type': 'date'}),
        }

class MicroblogForm(forms.ModelForm):
    class Meta:
        model = Microblog
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

