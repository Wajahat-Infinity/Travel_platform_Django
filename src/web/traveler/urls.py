from django.urls import path
from src.web.traveler.views import DashboardView


app_name = "traveler"

urlpatterns = [
    path('traveler/dashboard/', DashboardView.as_view(), name="dashboard"),
]
