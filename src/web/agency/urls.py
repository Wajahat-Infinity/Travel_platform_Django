from django.urls import path

from src.web.agency.views import DashboardView, BookingView, ProfileView, ReviewsView, WishlistView, SettingView, \
    OrdersView, TravellersView, TravelAgentsView, InvoicesView, PaymentsView, CurrencyView, SubscriberView, \
    LocationView, BranchesView, VehicleView, EditProfileView, BranchesAddView, BranchesUpdateView, BranchesDeleteView

app_name = "agency"

urlpatterns = [
    path('agency/dashboard/', DashboardView.as_view(), name="dashboard"),
    path('agency/booking/', BookingView.as_view(), name="booking"),
    path('agency/branches/', BranchesView.as_view(), name="branches"),
    path('agency/add/branch/', BranchesAddView.as_view(), name="add-branch"),
    path('agency/update/branch/<int:pk>/', BranchesUpdateView.as_view(), name="update-branch"),
    path('agency/delete/branch/<int:id>/', BranchesDeleteView.as_view(), name="delete-branch"),
    path('agency/orders/', OrdersView.as_view(), name="orders"),
    path('agency/vehicle/', VehicleView.as_view(), name="vehicle"),

    path('agency/travellers/', TravellersView.as_view(), name="travellers"),

    path('agency/profile/', ProfileView.as_view(), name="profile"),
    path('agency/edit/profile/', EditProfileView.as_view(), name="edit_profile"),
    path('agency/reviews/', ReviewsView.as_view(), name="reviews"),
    path('agency/wishlist/', WishlistView.as_view(), name="wishlist"),

    path('agency/travel-agents/', TravelAgentsView.as_view(), name="travel-agents"),

    path('agency/invoices/', InvoicesView.as_view(), name="invoices"),
    path('agency/payments/', PaymentsView.as_view(), name="payments"),
    path('agency/currency/', CurrencyView.as_view(), name="currency"),
    path('agency/subscriber/', SubscriberView.as_view(), name="subscriber"),

    path('agency/location/', LocationView.as_view(), name="location"),

    path('agency/setting/', SettingView.as_view(), name="setting"),
]
