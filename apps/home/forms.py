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
                "class": "form-control",
                "id": "repopinmodel-pin_code",
                "aria - required": "true",
            }
        ))
