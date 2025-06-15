from django.urls import path

from src.web.branches.views import DashboardView, BookingView, ProfileView, ReviewsView, SettingView, ProfileEditView

app_name = "branches"

urlpatterns = [
    path('branch/dashboard/', DashboardView.as_view(), name="dashboard"),
    path('branch/booking/', BookingView.as_view(), name="booking"),
    path('branch/profile/', ProfileView.as_view(), name="profile"),
    path('branch/edit/profile/', ProfileEditView.as_view(), name="edit-profile"),
    path('branch/reviews/', ReviewsView.as_view(), name="reviews"),
    path('branch/setting/', SettingView.as_view(), name="setting"),
]
