from django.forms import ModelForm
from django import forms
from src.accounts.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit

from src.web.agency.models import Agency, Vehicle
from src.web.local_guide.models import LocalGuide
from src.web.traveler.models import Traveler


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'profile_image', 'first_name', 'last_name',
            'phone_number'
        ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'country', 'profile_image']


class IncompleteAgencyForm(ModelForm):
    class Meta:
        model = Agency
        fields = '__all__'
        exclude = ['user', 'created_at', 'rating']  # Exclude auto-managed fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('license_number', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                Column('phone_number', css_class='form-group col-md-6'),
                Column('address', css_class='form-group col-md-12'),
                Row(
                    Column('city', css_class='form-group col-md-4'),
                    Column('state', css_class='form-group col-md-4'),
                    Column('zip_code', css_class='form-group col-md-2'),
                    Column('country', css_class='form-group col-md-2'),
                ),
                Column('description', css_class='form-group col-md-12'),
                Column('establish_year', css_class='form-group col-md-4'),
                Column('team_size', css_class='form-group col-md-4'),
                Column('website', css_class='form-group col-md-4'),
                Column('logo', css_class='form-group col-md-6'),
                Column('cover_image', css_class='form-group col-md-6'),
            ),
            Submit('submit', 'Submit', css_class='btn btn-success float-right')
        )


class IncompleteLocalGuideForm(ModelForm):
    class Meta:
        model = LocalGuide
        fields = '__all__'
        exclude = ['user', 'created_at', 'updated_at', 'rating']  # Exclude auto-managed fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6'),
                Column('phone', css_class='form-group col-md-6'),
                Column('address', css_class='form-group col-md-12'),
                Row(
                    Column('city', css_class='form-group col-md-4'),
                    Column('state', css_class='form-group col-md-4'),
                    Column('zip_code', css_class='form-group col-md-2'),
                    Column('country', css_class='form-group col-md-2'),
                ),
                Column('skills', css_class='form-group col-md-12'),
                Column('experience_years', css_class='form-group col-md-4'),
                Column('availability', css_class='form-group col-md-4'),
                Column('image', css_class='form-group col-md-6'),
                Column('cover_image', css_class='form-group col-md-6'),
            ),
            Submit('submit', 'Submit', css_class='btn btn-success float-right')
        )


class IncompleteTravelerForm(ModelForm):
    class Meta:
        model = Traveler
        fields = '__all__'
        exclude = ['user', 'created_at', 'updated_at', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6'),
                Column('phone_number', css_class='form-group col-md-6'),
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-md-4'),
                Column('gender', css_class='form-group col-md-4'),
                Column('profile_picture', css_class='form-group col-md-4'),
            ),
            Row(
                Column('address', css_class='form-group col-md-12'),
            ),
            Row(
                Column('city', css_class='form-group col-md-4'),
                Column('state', css_class='form-group col-md-4'),
                Column('zip_code', css_class='form-group col-md-2'),
                Column('country', css_class='form-group col-md-2'),
            ),
            Row(
                Column('passport_number', css_class='form-group col-md-6'),
                Column('passport_expiry', css_class='form-group col-md-6'),
            ),
            Row(
                Column('emergency_contact_name', css_class='form-group col-md-6'),
                Column('emergency_contact_phone', css_class='form-group col-md-6'),
            ),
            Row(
                Column('preferred_language', css_class='form-group col-md-4'),
                Column('dietary_restrictions', css_class='form-group col-md-4'),
                Column('special_needs', css_class='form-group col-md-4'),
            ),
            Submit('submit', 'Save Profile', css_class='btn btn-primary')
        )


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'