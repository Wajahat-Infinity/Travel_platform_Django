from django.contrib import admin
from .models import Agency, Hotel, HotelImage, Vehicle, Place, PlaceImage, TourPackage, TourBooking

admin.site.register(Agency)
admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(Vehicle)
admin.site.register(Place)
admin.site.register(PlaceImage)
admin.site.register(TourPackage)

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_number', 'tour_package', 'traveler', 'number_of_people', 'final_amount', 'status', 'payment_status', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', 'travel_date']
    search_fields = ['booking_number', 'tour_package__name', 'traveler__email', 'traveler__username']
    readonly_fields = ['booking_number', 'total_amount', 'discount_amount', 'final_amount', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_number', 'tour_package', 'traveler', 'status')
        }),
        ('Travel Details', {
            'fields': ('number_of_people', 'travel_date', 'special_requests')
        }),
        ('Pricing', {
            'fields': ('price_per_person', 'total_amount', 'discount_amount', 'final_amount')
        }),
        ('Payment Information', {
            'fields': ('stripe_payment_intent_id', 'stripe_charge_id', 'payment_status', 'payment_date')
        }),
        ('Cancellation', {
            'fields': ('cancelled_at', 'cancellation_reason', 'refund_amount'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )