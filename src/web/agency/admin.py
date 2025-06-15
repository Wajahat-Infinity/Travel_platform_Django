from django.contrib import admin
from .models import Agency, Hotel, HotelImage, Vehicle, Place, PlaceImage, TourPackage

admin.site.register(Agency)
admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(Vehicle)
admin.site.register(Place)
admin.site.register(PlaceImage)
admin.site.register(TourPackage)