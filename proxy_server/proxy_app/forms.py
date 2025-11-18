from django import forms
from .models import NetworkRule

class NetworkForm(forms.ModelForm):
    class Meta:
        model = NetworkRule
        fields = ['name', 'host', 'path_prefix', 'enable', 'response_code']
        widgets = {
            'response_body': forms.Textarea(attrs={'rows':4, 'cols':40})
        }