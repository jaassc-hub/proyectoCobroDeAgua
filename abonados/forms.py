from django import forms
from .models import Abonado

class AbonadoForm(forms.ModelForm):
    class Meta:
        model = Abonado
        fields = '__all__'