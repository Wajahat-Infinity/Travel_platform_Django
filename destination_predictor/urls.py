from django.urls import path
from . import views

app_name = 'destination_predictor'

urlpatterns = [
    path('predict/', views.predict_destination, name='predict'),
] 