from django import forms
from src.web.agency.models import TourBooking

class TourBookingForm(forms.ModelForm):
    class Meta:
        model = TourBooking
        fields = ['number_of_people', 'travel_date', 'special_requests']
        widgets = {
            'number_of_people': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '20',
                'placeholder': 'Number of people'
            }),
            'travel_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select travel date'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Any special requests or requirements...'
            })
        }

    def __init__(self, *args, **kwargs):
        self.tour_package = kwargs.pop('tour_package', None)
        super().__init__(*args, **kwargs)
        
        if self.tour_package:
            # Set minimum date to today
            from datetime import date
            self.fields['travel_date'].widget.attrs['min'] = date.today().isoformat()
            
            # Set maximum number of people based on tour package
            self.fields['number_of_people'].widget.attrs['max'] = '20'  # You can adjust this based on your business logic 