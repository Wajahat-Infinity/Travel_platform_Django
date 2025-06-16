from django import forms
from .models import LocalGuide, LocalGuideLanguage, LocalGuideCertification, GuideBooking
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

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

class GuideBookingForm(forms.ModelForm):
    class Meta:
        model = GuideBooking
        fields = ['start_date', 'end_date', 'number_of_people', 'special_requests']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.guide = kwargs.pop('guide', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('start_date', css_class='form-group col-md-6'),
                Column('end_date', css_class='form-group col-md-6'),
                Column('number_of_people', css_class='form-group col-md-6'),
                Column('special_requests', css_class='form-group col-md-12'),
            ),
            Submit('submit', 'Book Now', css_class='btn btn-success float-right')
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        number_of_people = cleaned_data.get('number_of_people')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date must be after start date")

            if self.guide and self.guide.availability == 'UNAVAILABLE':
                raise forms.ValidationError("This guide is currently unavailable")

        if number_of_people and number_of_people < 1:
            raise forms.ValidationError("Number of people must be at least 1")

        return cleaned_data