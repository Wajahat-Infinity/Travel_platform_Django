from django import forms
from .models import LocalGuide, LocalGuideLanguage, LocalGuideCertification

class LocalGuideForm(forms.ModelForm):
    class Meta:
        model = LocalGuide
        fields = '__all__'
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
    
    def clean_experience_years(self):
        years = self.cleaned_data.get('experience_years')
        if years < 0 or years > 100:
            raise forms.ValidationError("Experience years must be between 0 and 100")
        return years