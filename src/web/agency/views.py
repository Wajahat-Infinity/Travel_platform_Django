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
from src.web.agency.models import TourBooking
from django.http import Http404

class AgencyBaseView(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agency'] = self.request.user.agency
        return context

class AgencyDashboardView(LoginRequiredMixin, View):
    template_name = 'agency/dashboard.html'
    
    def get(self, request):
        agency = request.user.agency
        # Get all tour packages for this agency
        tour_packages = TourPackage.objects.filter(agency=agency)
        # Get all tour bookings for this agency's packages
        tour_bookings = TourBooking.objects.filter(tour_package__in=tour_packages)
        # Get total bookings (old + new)
        total_bookings = Booking.objects.filter(agency=agency).count() + tour_bookings.count()
        # Get total revenue (old + new)
        total_revenue = (Booking.objects.filter(agency=agency).aggregate(total=Sum('total_price'))['total'] or 0) + (tour_bookings.aggregate(total=Sum('final_amount'))['total'] or 0)
        # Get recent bookings (old + new, sorted by created_at)
        recent_bookings = list(Booking.objects.filter(agency=agency)) + list(tour_bookings)
        recent_bookings = sorted(recent_bookings, key=lambda b: b.created_at, reverse=True)[:5]
        # Get upcoming trips (old + new, confirmed only)
        upcoming_bookings = list(Booking.objects.filter(agency=agency, start_date__gte=timezone.now(), status='confirmed'))
        upcoming_tour_bookings = list(tour_bookings.filter(travel_date__gte=timezone.now().date(), status='confirmed'))
        upcoming_trips = sorted(upcoming_bookings + upcoming_tour_bookings, key=lambda b: b.created_at)[:5]
        # Get popular trips (old logic)
        popular_trips = Trip.objects.filter(agency=agency).annotate(booking_count=Count('bookings', distinct=True)).order_by('-booking_count')[:5]
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
    template_name = 'agency/booking_list.html'
    context_object_name = 'bookings'
    def get_queryset(self):
        agency = self.request.user.agency
        tour_packages = TourPackage.objects.filter(agency=agency)
        bookings = list(Booking.objects.filter(agency=agency))
        tour_bookings = list(TourBooking.objects.filter(tour_package__in=tour_packages))
        all_bookings = sorted(bookings + tour_bookings, key=lambda b: b.created_at, reverse=True)
        return all_bookings

class CustomerListView(AgencyBaseView, ListView):
    template_name = 'agency/customer_list.html'
    context_object_name = 'customers'
    def get_queryset(self):
        agency = self.request.user.agency
        tour_packages = TourPackage.objects.filter(agency=agency)
        # Travelers from old Booking model
        old_travelers = Traveler.objects.filter(bookings__agency=agency)
        # Travelers from new TourBooking model
        new_travelers = Traveler.objects.filter(user__tour_bookings__tour_package__in=tour_packages)
        # Combine and deduplicate
        all_travelers = old_travelers | new_travelers
        return all_travelers.distinct().order_by('user__first_name', 'user__last_name')

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
    fields = ['name', 'description', 'address', 'email', 'website', 'profile_image']
    success_url = reverse_lazy('agency:profile')

    def get_object(self, queryset=None):
        return self.request.user.agency

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['agency'] = self.request.user.agency
        return context

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
        agency = self.request.user.agency
        tour_packages = TourPackage.objects.filter(agency=agency)
        bookings = list(Booking.objects.filter(agency=agency))
        tour_bookings = list(TourBooking.objects.filter(tour_package__in=tour_packages))
        all_payments = sorted(bookings + tour_bookings, key=lambda b: b.created_at, reverse=True)
        return all_payments
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agency = self.request.user.agency
        tour_packages = TourPackage.objects.filter(agency=agency)
        bookings = Booking.objects.filter(agency=agency)
        tour_bookings = TourBooking.objects.filter(tour_package__in=tour_packages)
        context['total_revenue'] = (bookings.aggregate(total=Sum('total_price'))['total'] or 0) + (tour_bookings.aggregate(total=Sum('final_amount'))['total'] or 0)
        context['pending_payments'] = (bookings.filter(status='pending').aggregate(total=Sum('total_price'))['total'] or 0) + (tour_bookings.filter(status='pending').aggregate(total=Sum('final_amount'))['total'] or 0)
        context['completed_payments'] = (bookings.filter(status='completed').aggregate(total=Sum('total_price'))['total'] or 0) + (tour_bookings.filter(status='completed').aggregate(total=Sum('final_amount'))['total'] or 0)
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

class BookingDetailView(AgencyBaseView, View):
    template_name = 'agency/booking_detail.html'
    def get(self, request, type, booking_id):
        if type == 'old':
            booking = get_object_or_404(Booking, id=booking_id)
        elif type == 'tour':
            booking = get_object_or_404(TourBooking, id=booking_id)
        else:
            raise Http404('Invalid booking type')
        return render(request, self.template_name, {'booking': booking})

def confirm_booking(request, type, booking_id):
    if type == 'old':
        booking = get_object_or_404(Booking, id=booking_id)
    elif type == 'tour':
        booking = get_object_or_404(TourBooking, id=booking_id)
    else:
        raise Http404('Invalid booking type')
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, 'Booking confirmed!')
    return redirect('agency:booking_list')

def cancel_booking(request, type, booking_id):
    if type == 'old':
        booking = get_object_or_404(Booking, id=booking_id)
    elif type == 'tour':
        booking = get_object_or_404(TourBooking, id=booking_id)
    else:
        raise Http404('Invalid booking type')
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, 'Booking cancelled!')
    return redirect('agency:booking_list')