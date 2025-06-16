from django.urls import path
from src.web.traveler.views import (
    DashboardView, BookingView, FinanceView, SettingView,
    SavedTripsView, MyTripsView, ProfileView,
    cancel_booking, save_trip
)


app_name = "traveler"

urlpatterns = [
    path('traveler/dashboard/', DashboardView.as_view(), name="dashboard"),
    path('traveler/booking/', BookingView.as_view(), name="booking"),
    path('traveler/saved/', SavedTripsView.as_view(), name="saved"),
    path('traveler/trips/', MyTripsView.as_view(), name="trips"),
    path('traveler/finance/', FinanceView.as_view(), name="finance"),
    path('traveler/profile/', ProfileView.as_view(), name="profile"),
    path('traveler/settings/', SettingView.as_view(), name="settings"),
    path('traveler/booking/<int:booking_id>/cancel/', cancel_booking, name="cancel_booking"),
    path('traveler/trip/<int:trip_id>/save/', save_trip, name="save_trip"),
]
