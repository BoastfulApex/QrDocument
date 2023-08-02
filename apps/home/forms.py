from django import forms


class CreatePdfForm(forms.Form):
    file = forms.FileField()
    url = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Document ID si",
                "class": "form-control",
            }
        ))
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Document Kodi",
                "class": "form-control",
            }
        ))


class GetPinForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите PIN-код для просмотра документа",
                "class": "form-control",
            }
        ))
