from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from src.accounts.forms import IncompleteAgencyForm, UserForm, VehicleForm
from src.web.agency.models import Agency, Vehicle

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'traveler/dashboard.html'

