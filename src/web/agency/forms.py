from django import forms
from .models import TourPackage, Hotel, Vehicle, Place, HotelImage, PlaceImage

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = [
            'name', 'description', 'package_type', 'duration_days',
            'price', 'start_date', 'end_date',
             'vehicles', 'places', 'is_active'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        agency = kwargs.pop('agency', None)
        super().__init__(*args, **kwargs)
        if agency:
            # self.fields['hotels'].queryset = Hotel.objects.filter(agency=agency)
            self.fields['vehicles'].queryset = Vehicle.objects.filter(agency=agency)
            self.fields['places'].queryset = Place.objects.filter(agency=agency)

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'rating', 'price_range', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)]),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['model', 'capacity', 'registration_number', 'image']

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'location', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ['image', 'is_featured']

class PlaceImageForm(forms.ModelForm):
    class Meta:
        model = PlaceImage
        fields = ['image', 'is_featured'] 