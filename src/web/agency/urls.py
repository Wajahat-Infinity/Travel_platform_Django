from django.urls import path
from . import views

app_name = "agency"

urlpatterns = [
    # Dashboard
    path('dashboard/', views.AgencyDashboardView.as_view(), name='dashboard'),
   
    # path('agency/orders/', OrdersView.as_view(), name="orders"),
    # path('agency/vehicle/', VehicleView.as_view(), name="vehicle"),

    # path('agency/travellers/', TravellersView.as_view(), name="travellers"),

    # path('agency/profile/', ProfileView.as_view(), name="profile"),
    # path('agency/edit/profile/', EditProfileView.as_view(), name="edit_profile"),
    # path('agency/reviews/', ReviewsView.as_view(), name="reviews"),
    # path('agency/wishlist/', WishlistView.as_view(), name="wishlist"),

    # path('agency/travel-agents/', TravelAgentsView.as_view(), name="travel-agents"),

    # path('agency/invoices/', InvoicesView.as_view(), name="invoices"),
    # path('agency/payments/', PaymentsView.as_view(), name="payments"),
    # path('agency/currency/', CurrencyView.as_view(), name="currency"),
    # path('agency/subscriber/', SubscriberView.as_view(), name="subscriber"),

    # path('agency/location/', LocationView.as_view(), name="location"),

    # path('agency/setting/', SettingView.as_view(), name="setting"),

    # Bookings
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    
    # Customers
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    
    # Analytics
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    
    # Payments
    path('payments/', views.PaymentListView.as_view(), name='payments'),
    
    # Profile and Settings
    path('profile/', views.AgencyProfileView.as_view(), name='profile'),
    path('settings/', views.AgencySettingsView.as_view(), name='settings'),
    path('edit-profile/', views.AgencyEditProfileView.as_view(), name='edit_profile'),
    
    # Packages
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('packages/create/', views.PackageCreateView.as_view(), name='package_create'),
    path('packages/<int:pk>/edit/', views.PackageUpdateView.as_view(), name='package_edit'),
    path('packages/<int:pk>/delete/', views.PackageDeleteView.as_view(), name='package_delete'),
    
    # Hotels
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/create/', views.HotelCreateView.as_view(), name='hotel_create'),
    path('hotels/<int:pk>/edit/', views.HotelUpdateView.as_view(), name='hotel_edit'),
    path('hotels/<int:pk>/delete/', views.HotelDeleteView.as_view(), name='hotel_delete'),
    
    # Vehicles
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),

    path('places/', views.PlaceListView.as_view(), name='place_list'),
    path('places/create/', views.PlaceCreateView.as_view(), name='place_create'),
    path('places/<int:pk>/edit/', views.PlaceUpdateView.as_view(), name='place_edit'),
    path('places/<int:pk>/delete/', views.PlaceDeleteView.as_view(), name='place_delete'),
]
