from django.urls import path
from src.web.traveler.views import DashboardView, BookingView, FinanceView, SettingView


app_name = "traveler"

urlpatterns = [
    path('traveler/dashboard/', DashboardView.as_view(), name="dashboard"),
    path('traveler/booking/', BookingView.as_view(), name="booking"),
    path('traveler/finance/', FinanceView.as_view(), name="finance"),
    path('traveler/settings/', SettingView.as_view(), name="settings"),
]
