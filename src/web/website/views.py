from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from src.web.agency.models import Vehicle, Agency
from src.web.local_guide.models import LocalGuide

# Create your views here.

class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agencies'] = Agency.objects.all()
        return context


class AgencyView(ListView):
    model = Agency
    context_object_name = 'agencies'
    template_name = 'website/agencies.html'


class AgencyDetailView(DetailView):
    model = Agency
    context_object_name = 'agency'
    template_name = 'website/agency_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.filter(object_id=self.object.id)
        context['schedules'] = Schedule.objects.filter(vehicle__object_id=self.object.id)
        context['branches'] = Branch.objects.filter(agency=self.object)
        return context



class VehicleDetailView(DetailView):
    model = Vehicle
    context_object_name = 'vehicle'
    template_name = 'website/vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedule'] = Schedule.objects.filter(vehicle=self.object)
        return context


class AboutView(TemplateView):
    template_name = 'website/about.html'


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class FaqView(TemplateView):
    template_name = 'website/faq.html'


class LocalGuideView(ListView):
    model = LocalGuide
    template_name = 'website/local_guide.html'
    context_object_name = 'local_guide'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['local_guide'] = LocalGuide.objects.all()
        return context


class LocalGuideDetailView(DetailView):
    model = LocalGuide
    template_name = 'website/local_guide_detail.html'
    context_object_name = 'guide'


class CheckoutView(TemplateView):
    template_name = 'website/checkout.html'


class LoginView(TemplateView):
    template_name = 'account/login.html'


class SignupView(TemplateView):
    template_name = 'account/signup.html'


class ForgetPasswordView(TemplateView):
    template_name = 'account/password_reset.html'
