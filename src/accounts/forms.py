from django.forms import ModelForm
from django import forms
from src.accounts.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit

from src.web.agency.models import Agency, Branch, Vehicle


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
        fields = ['name',
                  'logo', 'cover_image', 'tagline', 'description', 'contact_email',
                  'company_registration_number', 'vat_number',
                  'address', 'contact_phone', 'company_postal_code',
                  'company_city', 'company_state',
                  'website', 'instagram', 'facebook', 'twitter'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-sm-4'),
                Column('company_registration_number', css_class='form-group col-sm-4'),
                Column('vat_number', css_class='form-group col-sm-4'),
                Column('tagline', css_class='form-group col-sm-6'),
                Column('logo', css_class='form-group col-sm-6'),
                Column('cover_image', css_class='form-group col-sm-6'),
                Column('contact_email', css_class='col-sm-6'),
                Column('contact_phone', css_class='col-sm-6'),
                Column('address', css_class='col-sm-6 '),
                Column('company_postal_code', css_class='col-sm-6'),
                Column('company_city', css_class='col-sm-4'),
                Column('company_state', css_class='col-sm-4'),
                Column('website', css_class='col-sm-3'),
                Column('instagram', css_class='col-sm-3'),
                Column('facebook', css_class='col-sm-3'),
                Column('twitter', css_class='col-sm-3'),
                Column('description', css_class='col-sm-12'),
            ),
            Submit('submit', 'Submit', css_class='btn btn-success float-right')
        )


class IncompleteBranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = ['name',
                  'cover_image', 'description', 'contact_email',
                  'registration_number',
                  'address', 'contact_phone',
                  'location', 'is_active',
                  ]


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'model', 'capacity', 'image', 'is_active']
