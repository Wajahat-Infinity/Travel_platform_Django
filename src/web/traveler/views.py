from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.utils import timezone
from django import forms

from src.accounts.forms import IncompleteAgencyForm, UserForm, VehicleForm
from src.web.agency.models import Agency, Vehicle, TourBooking
from src.web.traveler.models import Traveler
from src.web.booking.models import Booking, Trip
from src.web.local_guide.models import GuideBooking

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


class TravelerBaseView(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traveler = get_object_or_404(Traveler, user=self.request.user)
        context['traveler'] = traveler
        
        # Get active bookings (old booking system)
        active_bookings = Booking.objects.filter(
            traveler=traveler,
            status__in=['confirmed', 'pending']
        ).order_by('-created_at')
        
        # Get active tour bookings (new booking system)
        active_tour_bookings = TourBooking.objects.filter(
            traveler=self.request.user,
            status__in=['confirmed', 'pending']
        ).order_by('-created_at')
        
        # Get booking statistics
        booking_stats = {
            'total': Booking.objects.filter(traveler=traveler).count(),
            'active': active_bookings.count(),
            'completed': Booking.objects.filter(traveler=traveler, status='completed').count(),
            'cancelled': Booking.objects.filter(traveler=traveler, status='cancelled').count(),
            'confirmed': Booking.objects.filter(traveler=traveler, status='confirmed').count(),
        }
        
        # Get tour booking statistics
        tour_booking_stats = {
            'total': TourBooking.objects.filter(traveler=self.request.user).count(),
            'active': active_tour_bookings.count(),
            'completed': TourBooking.objects.filter(traveler=self.request.user, status='completed').count(),
            'cancelled': TourBooking.objects.filter(traveler=self.request.user, status='cancelled').count(),
            'confirmed': TourBooking.objects.filter(traveler=self.request.user, status='confirmed').count(),
        }
        
        context['booking_stats'] = booking_stats
        context['tour_booking_stats'] = tour_booking_stats
        context['active_bookings'] = active_bookings[:5]  # Show only 5 most recent active bookings
        context['active_tour_bookings'] = active_tour_bookings[:5]  # Show only 5 most recent active tour bookings
        context['guide_bookings'] = GuideBooking.objects.filter(
            traveler=traveler,
            status__in=['pending', 'confirmed']
        ).order_by('-created_at')[:5]
        return context


@method_decorator(login_required, name='dispatch')
class DashboardView(TravelerBaseView, TemplateView):
    template_name = 'traveler/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traveler = context['traveler']
        
        # Get recent bookings (old system)
        recent_bookings = Booking.objects.filter(
            traveler=traveler
        ).order_by('-created_at')[:5]
        
        # Get recent tour bookings (new system)
        recent_tour_bookings = TourBooking.objects.filter(
            traveler=self.request.user
        ).order_by('-created_at')[:5]
        
        # Get upcoming trips (old system)
        upcoming_trips = Booking.objects.filter(
            traveler=traveler,
            start_date__gte=timezone.now(),
            status='confirmed'
        ).order_by('start_date')[:3]
        
        # Get upcoming tour trips (new system)
        upcoming_tour_trips = TourBooking.objects.filter(
            traveler=self.request.user,
            travel_date__gte=timezone.now().date(),
            status='confirmed'
        ).order_by('travel_date')[:3]
        
        context.update({
            'recent_bookings': recent_bookings,
            'recent_tour_bookings': recent_tour_bookings,
            'upcoming_trips': upcoming_trips,
            'upcoming_tour_trips': upcoming_tour_trips,
            'total_bookings': Booking.objects.filter(traveler=traveler).count(),
            'total_tour_bookings': TourBooking.objects.filter(traveler=self.request.user).count(),
            'total_guide_bookings': GuideBooking.objects.filter(traveler=traveler).count(),
            'completed_trips': Booking.objects.filter(
                traveler=traveler,
                status='completed'
            ).count(),
            'completed_tour_trips': TourBooking.objects.filter(
                traveler=self.request.user,
                status='completed'
            ).count(),
        })
        return context


@method_decorator(login_required, name='dispatch')
class BookingView(ListView):
    template_name = 'traveler/booking.html'
    context_object_name = 'bookings'
    model = TourBooking

    def get_queryset(self):
        # self.request.user must be a User object
        user = self.request.user

        # This must pass a User instance, not a string
        traveler = get_object_or_404(Traveler, user=user)

        # Optional filter
        status = self.request.GET.get('status')

        # Use User object directly in TourBooking query
        queryset = TourBooking.objects.filter(traveler=user)

        if status:
            queryset = queryset.filter(status=status)

        return queryset


@method_decorator(login_required, name='dispatch')
class SavedTripsView(TravelerBaseView, ListView):
    template_name = 'traveler/saved.html'
    context_object_name = 'saved_trips'
    paginate_by = 10
    
    def get_queryset(self):
        traveler = get_object_or_404(Traveler, user=self.request.user)
        return traveler.saved_trips.all()


@method_decorator(login_required, name='dispatch')
class MyTripsView(TravelerBaseView, ListView):
    template_name = 'traveler/trips.html'
    context_object_name = 'trips'
    paginate_by = 10
    
    def get_queryset(self):
        traveler = get_object_or_404(Traveler, user=self.request.user)
        return Booking.objects.filter(
            traveler=traveler,
            status='confirmed'
        ).select_related('trip')


@method_decorator(login_required, name='dispatch')
class FinanceView(TravelerBaseView, ListView):
    template_name = 'traveler/invoices.html'
    context_object_name = 'invoices'
    paginate_by = 10
    
    def get_queryset(self):
        traveler = get_object_or_404(Traveler, user=self.request.user)
        return Booking.objects.filter(
            traveler=traveler,
            status__in=['completed', 'confirmed']
        ).order_by('-created_at')


@method_decorator(login_required, name='dispatch')
class ProfileView(TravelerBaseView, TemplateView):
    template_name = 'traveler/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traveler = context['traveler']
        
        # Get booking history
        all_bookings = Booking.objects.filter(traveler=traveler).order_by('-created_at')
        booking_history = all_bookings[:10]
        completed_trips_count = all_bookings.filter(status='completed').count()
        
        context['bookings'] = booking_history
        context['guide_bookings'] = GuideBooking.objects.filter(
            traveler=traveler
        ).order_by('-created_at')
        context['total_bookings'] = all_bookings.count()
        context['completed_trips'] = completed_trips_count
        return context


class TravelerUpdateForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = ['full_name', 'date_of_birth', 'gender', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country', 'passport_number', 'passport_expiry', 'preferred_language', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'passport_expiry': forms.DateInput(attrs={'type': 'date'}),
        }


@method_decorator(login_required, name='dispatch')
class SettingView(TravelerBaseView, View):
    template_name = 'traveler/setting.html'

    def get(self, request):
        traveler = request.user.traveler_profile
        form = TravelerUpdateForm(instance=traveler)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        traveler = request.user.traveler_profile
        form = TravelerUpdateForm(request.POST, request.FILES, instance=traveler)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('traveler:settings')
        return render(request, self.template_name, {'form': form})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, traveler=request.user.traveler_profile)
    
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'Only pending bookings can be cancelled.')
    
    return redirect('traveler:dashboard')


@login_required
def save_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    traveler = request.user.traveler_profile
    if trip not in traveler.saved_trips.all():
        traveler.saved_trips.add(trip)
        messages.success(request, 'Trip saved successfully.')
    else:
        traveler.saved_trips.remove(trip)
        messages.success(request, 'Trip removed from saved trips.')
    
    return redirect('traveler:saved-trips')

