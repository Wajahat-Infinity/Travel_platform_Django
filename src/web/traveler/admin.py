from django.contrib import admin
from .models import Traveler

@admin.register(Traveler)
class TravelerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'phone_number', 'country', 'created_at')
    list_filter = ('country', 'gender', 'created_at')
    search_fields = ('full_name', 'user__email', 'phone_number', 'passport_number')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'user', 'full_name', 'date_of_birth', 'gender', 
                'profile_picture', 'phone_number'
            )
        }),
        ('Address Information', {
            'fields': (
                'address', 'city', 'state', 
                'zip_code', 'country'
            )
        }),
        ('Travel Documents', {
            'fields': (
                'passport_number', 'passport_expiry'
            )
        }),
        ('Emergency Contacts', {
            'fields': (
                'emergency_contact_name', 'emergency_contact_phone'
            )
        }),
        ('Preferences & Needs', {
            'fields': (
                'preferred_language', 'dietary_restrictions', 
                'special_needs'
            )
        }),
        ('Metadata', {
            'fields': (
                'created_at', 'updated_at'
            )
        }),
    )
    ordering = ('-created_at',)

