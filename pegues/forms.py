from django import forms
from .models import Pegue

class PegueForm(forms.ModelForm):
    class Meta:
        model = Pegue
        fields = '__all__'
        widgets = {
            'servicios': forms.CheckboxSelectMultiple(),
        }