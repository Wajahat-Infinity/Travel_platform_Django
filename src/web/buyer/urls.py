from django.urls import path

from src.web.buyer.views import DashboardView, BookingView, ProfileView, ReviewsView, WishlistView, SettingView, \
    PasswordChangeCustomView

app_name = "buyer"

urlpatterns = [
    path('user/dashboard/', DashboardView.as_view(), name="dashboard"),
    path('user/booking/', BookingView.as_view(), name="booking"),
    path('user/profile/', ProfileView.as_view(), name="profile"),
    path('user/reviews/', ReviewsView.as_view(), name="reviews"),
    path('user/wishlist/', WishlistView.as_view(), name="wishlist"),
    path('user/setting/', SettingView.as_view(), name="setting"),
    path('user/password/change/', PasswordChangeCustomView.as_view(), name="password_change"),
]
