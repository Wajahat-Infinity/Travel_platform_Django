from django.urls import path
from src.web.website.views import HomeView, AgencyView, AboutView, ContactView, FaqView, LoginView, SignupView, \
    ForgetPasswordView, CheckoutView, AgencyDetailView, VehicleDetailView,  \
    LocalGuideView, LocalGuideDetailView, NewsletterSubscribeView, TourDetailView,PackagesView

app_name = "website"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('agency/', AgencyView.as_view(), name="agency"),
    path('packages/', PackagesView.as_view(), name="packages"),
    path('agency/details/<int:pk>/', AgencyDetailView.as_view(), name="agency-detail"),
    path('agency/vehicle/details/<int:pk>/', VehicleDetailView.as_view(), name="vehicle-detail"),
    path('tour/<int:pk>/', TourDetailView.as_view(), name="tour_detail"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('faq/', FaqView.as_view(), name="faq"),
    path('local-guide/', LocalGuideView.as_view(), name="local_guide"),
    path('local-guide/<int:pk>/', LocalGuideDetailView.as_view(), name="local_guide_detail"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name="newsletter_subscribe"),
]
