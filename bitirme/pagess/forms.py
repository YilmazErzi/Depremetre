# forms.py
from django import forms
from .models import BuildingAssessment

class BuildingAssessmentForm(forms.ModelForm):
    class Meta:
        model = BuildingAssessment
        fields = ['building_name', 'score_year', 'score_ground', 'score_soft_story', 'score_damage', 'score_floor', 'score_shape']
        widgets = {
            'building_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Evim, İşyerim'}),
            # RadioSelect kullanarak seçenekleri açılır liste değil, şık butonlar olarak gösterelim
            'score_year': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'score_ground': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'score_soft_story': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'score_damage': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'score_floor': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'score_shape': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }