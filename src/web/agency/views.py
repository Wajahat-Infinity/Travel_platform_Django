from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from .models import TourPackage, Hotel, Vehicle, Place, HotelImage, PlaceImage, Agency
from .forms import TourPackageForm, HotelForm, VehicleForm, PlaceForm, HotelImageForm, PlaceImageForm
from src.web.booking.models import Booking, Trip
from src.web.traveler.models import Traveler

class AgencyBaseView(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agency'] = self.request.user.agency
        return context

class AgencyDashboardView(LoginRequiredMixin, View):
    template_name = 'agency/dashboard.html'
    
    def get(self, request):
        agency = request.user.agency
        
        # Get total bookings
        total_bookings = Booking.objects.filter(agency=agency).count()
        
        # Get total revenue
        total_revenue = Booking.objects.filter(agency=agency).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # Get recent bookings
        recent_bookings = Booking.objects.filter(agency=agency).order_by('-created_at')[:5]
        
        # Get upcoming trips
        upcoming_trips = Booking.objects.filter(
            agency=agency,
            start_date__gte=timezone.now(),
            status='confirmed'
        ).order_by('start_date')[:5]
        
        # Get popular trips
        popular_trips = Trip.objects.filter(
            agency=agency
        ).annotate(
            booking_count=Count('bookings', distinct=True)
        ).order_by('-booking_count')[:5]
        
        context = {
            'agency': agency,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue,
            'recent_bookings': recent_bookings,
            'upcoming_trips': upcoming_trips,
            'popular_trips': popular_trips,
        }
        
        return render(request, self.template_name, context)

class BookingListView(AgencyBaseView, ListView):
    model = Booking
    template_name = 'agency/booking_list.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        return Booking.objects.filter(agency=self.request.user.agency).order_by('-created_at')

class CustomerListView(AgencyBaseView, ListView):
    model = Traveler
    template_name = 'agency/customer_list.html'
    context_object_name = 'customers'
    
    def get_queryset(self):
        # Get all travelers who have made bookings with this agency
        return Traveler.objects.filter(
            bookings__agency=self.request.user.agency
        ).distinct().order_by('user__first_name', 'user__last_name')

class AnalyticsView(AgencyBaseView, TemplateView):
    template_name = 'agency/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agency = self.request.user.agency
        
        # Get date range for analytics (last 30 days)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Get booking statistics
        bookings = Booking.objects.filter(
            agency=agency,
            created_at__range=(start_date, end_date)
        )
        
        # Total bookings and revenue
        context['total_bookings'] = bookings.count()
        context['total_revenue'] = bookings.aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # Average booking value
        context['avg_booking_value'] = bookings.aggregate(
            avg=Avg('total_price')
        )['avg'] or 0
        
        # Booking status distribution
        context['status_distribution'] = bookings.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Popular trips
        context['popular_trips'] = Trip.objects.filter(
            agency=agency,
            bookings__created_at__range=(start_date, end_date)
        ).annotate(
            booking_count=Count('bookings', distinct=True),
            revenue=Sum('bookings__total_price')
        ).order_by('-booking_count')[:5]
        
        # Customer statistics
        context['total_customers'] = Traveler.objects.filter(
            bookings__agency=agency,
            bookings__created_at__range=(start_date, end_date)
        ).distinct().count()
        
        return context

class AgencyProfileView(AgencyBaseView, TemplateView):
    template_name = 'agency/profile.html'

class AgencySettingsView(AgencyBaseView, TemplateView):
    template_name = 'agency/settings.html'

class AgencyEditProfileView(AgencyBaseView, UpdateView):
    model = Agency
    template_name = 'agency/edit_profile.html'
    fields = ['name', 'description', 'address', 'phone', 'email', 'website', 'profile_image']
    success_url = reverse_lazy('agency:profile')

    def get_object(self, queryset=None):
        return self.request.user.agency

    def post(self, request, *args, **kwargs):
        agency = request.user.agency
        # Handle form submission for profile update
        messages.success(request, 'Profile updated successfully!')
        return redirect('agency:profile')

# Package Views
class PackageListView(AgencyBaseView, ListView):
    model = TourPackage
    template_name = 'agency/packages.html'
    context_object_name = 'packages'

    def get_queryset(self):
        return TourPackage.objects.filter(agency=self.request.user.agency)

class PackageCreateView(AgencyBaseView, CreateView):
    model = TourPackage
    form_class = TourPackageForm
    template_name = 'agency/package_form.html'
    success_url = reverse_lazy('agency:package_list')

    def form_valid(self, form):
        form.instance.agency = self.request.user.agency
        messages.success(self.request, 'Tour package created successfully!')
        return super().form_valid(form)

class PackageUpdateView(AgencyBaseView, UpdateView):
    model = TourPackage
    form_class = TourPackageForm
    template_name = 'agency/package_form.html'
    success_url = reverse_lazy('agency:package_list')

    def get_queryset(self):
        return TourPackage.objects.filter(agency=self.request.user.agency)

    def form_valid(self, form):
        messages.success(self.request, 'Tour package updated successfully!')
        return super().form_valid(form)

class PackageDeleteView(AgencyBaseView, DeleteView):
    model = TourPackage
    template_name = 'agency/package_confirm_delete.html'
    success_url = reverse_lazy('agency:package_list')

    def get_queryset(self):
        return TourPackage.objects.filter(agency=self.request.user.agency)

# Vehicle Views
class VehicleListView(AgencyBaseView, ListView):
    model = Vehicle
    template_name = 'agency/vehicles.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        return Vehicle.objects.filter(agency=self.request.user.agency)

class VehicleCreateView(AgencyBaseView, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'agency/vehicle_form.html'
    success_url = reverse_lazy('agency:vehicle_list')

    def form_valid(self, form):
        form.instance.agency = self.request.user.agency
        messages.success(self.request, 'Vehicle added successfully!')
        return super().form_valid(form)

class VehicleUpdateView(AgencyBaseView, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'agency/vehicle_form.html'
    success_url = reverse_lazy('agency:vehicle_list')

    def get_queryset(self):
        return Vehicle.objects.filter(agency=self.request.user.agency)

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle updated successfully!')
        return super().form_valid(form)

class VehicleDeleteView(AgencyBaseView, DeleteView):
    model = Vehicle
    template_name = 'agency/vehicle_confirm_delete.html'
    success_url = reverse_lazy('agency:vehicle_list')

    def get_queryset(self):
        return Vehicle.objects.filter(agency=self.request.user.agency)

# Hotel Views
class HotelListView(AgencyBaseView, ListView):
    model = Hotel
    template_name = 'agency/hotels.html'
    context_object_name = 'hotels'

    def get_queryset(self):
        return Hotel.objects.filter(agency=self.request.user.agency)

class HotelCreateView(AgencyBaseView, CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'agency/hotel_form.html'
    success_url = reverse_lazy('agency:hotel_list')

    def form_valid(self, form):
        form.instance.agency = self.request.user.agency
        response = super().form_valid(form)
        # Handle multiple images
        for image in self.request.FILES.getlist('images'):
            HotelImage.objects.create(hotel=self.object, image=image)
        messages.success(self.request, 'Hotel added successfully!')
        return response

class HotelUpdateView(AgencyBaseView, UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = 'agency/hotel_form.html'
    success_url = reverse_lazy('agency:hotel_list')

    def get_queryset(self):
        return Hotel.objects.filter(agency=self.request.user.agency)

    def form_valid(self, form):
        messages.success(self.request, 'Hotel updated successfully!')
        return super().form_valid(form)

class HotelDeleteView(AgencyBaseView, DeleteView):
    model = Hotel
    template_name = 'agency/hotel_confirm_delete.html'
    success_url = reverse_lazy('agency:hotel_list')

    def get_queryset(self):
        return Hotel.objects.filter(agency=self.request.user.agency)

class PaymentListView(AgencyBaseView, ListView):
    template_name = 'agency/payment_list.html'
    context_object_name = 'payments'
    
    def get_queryset(self):
        # Get all bookings with their payment information
        return Booking.objects.filter(
            agency=self.request.user.agency
        ).select_related(
            'traveler',
            'trip'
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get payment statistics
        context['total_revenue'] = self.get_queryset().aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        context['pending_payments'] = self.get_queryset().filter(
            status='pending'
        ).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        context['completed_payments'] = self.get_queryset().filter(
            status='completed'
        ).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        return context

# Place Views
class PlaceListView(AgencyBaseView, ListView):
    model = Place
    template_name = 'agency/places.html'
    context_object_name = 'places'

    def get_queryset(self):
        return Place.objects.filter(agency=self.request.user.agency)

class PlaceCreateView(AgencyBaseView, CreateView):
    model = Place
    form_class = PlaceForm
    template_name = 'agency/place_form.html'
    success_url = reverse_lazy('agency:place_list')

    def form_valid(self, form):
        form.instance.agency = self.request.user.agency
        response = super().form_valid(form)
        # Handle multiple images
        for image in self.request.FILES.getlist('images'):
            PlaceImage.objects.create(place=self.object, image=image)
        messages.success(self.request, 'Place added successfully!')
        return response

class PlaceUpdateView(AgencyBaseView, UpdateView):
    model = Place
    form_class = PlaceForm
    template_name = 'agency/place_form.html'
    success_url = reverse_lazy('agency:place_list')

    def get_queryset(self):
        return Place.objects.filter(agency=self.request.user.agency)

    def form_valid(self, form):
        messages.success(self.request, 'Place updated successfully!')
        return super().form_valid(form)

class PlaceDeleteView(AgencyBaseView, DeleteView):
    model = Place
    template_name = 'agency/place_confirm_delete.html'
    success_url = reverse_lazy('agency:place_list')

    def get_queryset(self):
        return Place.objects.filter(agency=self.request.user.agency)