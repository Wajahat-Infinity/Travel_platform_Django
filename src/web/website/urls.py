from django.urls import path
from src.web.website.views import HomeView, AgencyView, AboutView, ContactView, FaqView, LoginView, SignupView, \
    ForgetPasswordView, CheckoutView, AgencyDetailView, VehicleDetailView,  \
    LocalGuideView, LocalGuideDetailView

app_name = "website"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('agency/', AgencyView.as_view(), name="agency"),
    path('agency/details/<int:pk>/', AgencyDetailView.as_view(), name="agency-detail"),
    path('agency/vehicle/details/<int:pk>/', VehicleDetailView.as_view(), name="vehicle-detail"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('faq/', FaqView.as_view(), name="faq"),
    path('local-guide/', LocalGuideView.as_view(), name="local_guide"),
    path('local-guide/<int:pk>/', LocalGuideDetailView.as_view(), name="local_guide_detail"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
]
