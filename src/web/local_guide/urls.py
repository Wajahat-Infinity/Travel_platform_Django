from django.urls import path
from . import views

app_name = 'local_guide'

urlpatterns = [
    path('guides/dashboard/', views.LocalGuideDashboardView.as_view(), name='dashboard'),
    path('guides/bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('guides/bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking_detail'),
    path('guides/bookings/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('guides/payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('guides/travelers/', views.TravellerListView.as_view(), name='traveller_list'),
    path('guides/tours/', views.TourListView.as_view(), name='tour_list'),
    path('guides/settings/', views.SettingsView.as_view(), name='settings'),
]