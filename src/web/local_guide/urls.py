from django.urls import path
from .views import LocalGuideListView, LocalGuideCreateView, LocalGuideDetailView,LocalGuideDashboardView

app_name = "local_guide"


urlpatterns = [
    path('guides/dashboard/', LocalGuideDashboardView.as_view(), name='dashboard'),
    path('guides/', LocalGuideListView.as_view(), name='localguide-list'),
    path('guides/create/', LocalGuideCreateView.as_view(), name='localguide-create'),
    path('guides/<int:pk>/', LocalGuideDetailView.as_view(), name='localguide-detail'),
]