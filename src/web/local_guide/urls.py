from django.urls import path
from .views import (
    LocalGuideListView, LocalGuideCreateView, LocalGuideDetailView,
    LocalGuideDashboardView, BookGuideView, BookingSuccessView
)

app_name = "local_guide"

urlpatterns = [
    path('guides/dashboard/', LocalGuideDashboardView.as_view(), name='dashboard'),
    path('guides/', LocalGuideListView.as_view(), name='localguide-list'),
    path('guides/create/', LocalGuideCreateView.as_view(), name='localguide-create'),
    path('guides/<int:pk>/', LocalGuideDetailView.as_view(), name='localguide-detail'),
    path('guides/<int:guide_id>/book/', BookGuideView.as_view(), name='book-guide'),
    path('bookings/<int:pk>/success/', BookingSuccessView.as_view(), name='booking-success'),
]