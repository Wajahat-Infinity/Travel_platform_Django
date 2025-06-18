from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from src.web.agency.models import Vehicle, Agency, Schedule, Branch, TourPackage
from src.web.local_guide.models import LocalGuide
from .models import (
    HeroSlider, PopularTour, TopActivity, BlogPost, 
    ClientLogo, NewsletterSubscriber, Testimonial, SiteSettings
)

# Create your views here.

class HomeView(TemplateView):
    template_name = 'website/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get site settings
        context['site_settings'] = SiteSettings.get_settings()
        
        # Get hero sliders
        context['hero_sliders'] = HeroSlider.objects.filter(is_active=True).order_by('order')
        
        # Get popular tours
        context['popular_tours'] = PopularTour.objects.filter(is_active=True).order_by('order')[:6]
        
        # Get top activities
        context['top_activities'] = TopActivity.objects.filter(is_active=True).order_by('order')[:8]
        
        # Get recent blog posts
        context['recent_posts'] = BlogPost.objects.filter(is_published=True).order_by('-published_date')[:3]
        
        # Get testimonials (keeping as requested)
        context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('order')
        
        # Get client logos
        context['client_logos'] = ClientLogo.objects.filter(is_active=True).order_by('order')
        
        # Get agencies for other sections
        context['agencies'] = Agency.objects.all()
        
        return context


class TourDetailView(DetailView):
    model = TourPackage
    template_name = 'website/tour_detail.html'
    context_object_name = 'tour_package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get similar tours (same agency, different packages)
        context['similar_tours'] = TourPackage.objects.filter(
            agency=self.object.agency,
            is_active=True
        ).exclude(id=self.object.id)[:3]
        
        return context


class AgencyView(ListView):
    model = Agency
    context_object_name = 'agencies'
    template_name = 'website/agencies.html'
    

class PackagesView(ListView):
    template_name = 'website/packages.html'
    model = PopularTour  # Replace with your actual model
    context_object_name = 'packages'  # Optional: gives a better name in template
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_tours'] = PopularTour.objects.filter(is_active=True).order_by('order')[:6]
        return context

class AgencyDetailView(DetailView):
    model = Agency
    context_object_name = 'agency'
    template_name = 'website/agency_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all related data for the agency
        context['vehicles'] = self.object.vehicles.all()
        context['schedules'] = Schedule.objects.filter(vehicle__agency=self.object)
        context['branches'] = self.object.branches.all()
        context['hotels'] = self.object.hotels.filter(is_active=True)
        context['places'] = self.object.places.all()
        context['tour_packages'] = self.object.tour_packages.filter(is_active=True)
        
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


@method_decorator(csrf_exempt, name='dispatch')
class NewsletterSubscribeView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            if email:
                subscriber, created = NewsletterSubscriber.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
                
                if created:
                    return JsonResponse({
                        'success': True,
                        'message': 'Successfully subscribed to newsletter!'
                    })
                else:
                    if subscriber.is_active:
                        return JsonResponse({
                            'success': False,
                            'message': 'You are already subscribed to our newsletter.'
                        })
                    else:
                        subscriber.is_active = True
                        subscriber.save()
                        return JsonResponse({
                            'success': True,
                            'message': 'Successfully re-subscribed to newsletter!'
                        })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Email is required.'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            })
