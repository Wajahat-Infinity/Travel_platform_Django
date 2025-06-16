from django.contrib import admin
from .models import Booking, Trip

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'traveler', 'trip', 'start_date', 'end_date', 'status', 'total_price')
    list_filter = ('status', 'start_date', 'agency')
    search_fields = ('booking_number', 'traveler__full_name', 'trip__title')
    readonly_fields = ('booking_number', 'created_at', 'updated_at')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_number', 'traveler', 'agency', 'trip', 'status')
        }),
        ('Trip Details', {
            'fields': ('start_date', 'end_date', 'number_of_people', 'total_price')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'created_at', 'updated_at')
        }),
    )

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'agency', 'destination', 'duration', 'price_per_person', 'max_people', 'is_active')
    list_filter = ('is_active', 'agency', 'destination')
    search_fields = ('title', 'description', 'destination')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('title', 'agency', 'description', 'destination', 'image')
        }),
        ('Trip Details', {
            'fields': ('duration', 'price_per_person', 'max_people', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    ) 