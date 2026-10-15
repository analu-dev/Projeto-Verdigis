from django import forms
from .models import Meta

#fabrica de metas!!
class FormsMetas(forms.ModelForm):
    class Meta:
        model =  Meta
        fields = ['nome', 'tipo_esg', 'deadline', 'resumo', 'prioridade'] #será preenchido!!
        
        # 'widgets' definem o tipo de elemento HTML de cada campo
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Reduzir uso de papel'}),
            'tipo_esg': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'resumo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Descrição da meta...'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
        }
