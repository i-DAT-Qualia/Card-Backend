from django import forms

class UploadScansForm(forms.Form):
    scan_file  = forms.FileField()