from django.urls import path, include
from .views import LogoutView, CrossAuthView, UserUpdateView, IdentificationCheck, ProfileCompleteView, LocalGuideCompleteView, TravelerCompleteView

app_name = 'accounts'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/change/', UserUpdateView.as_view(), name='user-change'),
    path('cross-auth/', CrossAuthView.as_view(), name='cross-auth'),

    path('identify/', IdentificationCheck.as_view(), name='identity-check'),
    path('agency/completation/', ProfileCompleteView.as_view(), name='vendor-complete'),
    path('local-guide/completation/', LocalGuideCompleteView.as_view(), name='local-guide-complete'),
    path('traveler/completation/', TravelerCompleteView.as_view(), name='traveler-complete'),
]


