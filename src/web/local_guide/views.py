from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from .models import LocalGuide, GuideBooking, Language, LocalGuideLanguage, LocalGuideCertification
from .forms import LocalGuideForm, GuideBookingForm
import os

class LocalGuideDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'local_guide/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        guide = get_object_or_404(LocalGuide, user=self.request.user)
        
        # Get statistics
        context['total_bookings'] = GuideBooking.objects.filter(guide=guide).count()
        context['active_bookings'] = GuideBooking.objects.filter(
            guide=guide,
            status__in=['pending', 'confirmed'],
            end_date__gte=timezone.now().date()
        ).count()
        
        # Get total reviews count
        context['total_reviews'] = guide.reviews.count() if hasattr(guide, 'reviews') else 0
        
        # Get total earnings (confirmed + completed)
        context['total_earnings'] = GuideBooking.objects.filter(
            guide=guide,
            status__in=['confirmed', 'completed']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        
        # Get recent bookings
        context['recent_bookings'] = GuideBooking.objects.filter(
            guide=guide
        ).select_related(
            'traveler',
            'traveler__user'
        ).order_by('-created_at')[:5]
        
        # Get recent reviews if reviews exist
        if hasattr(guide, 'reviews'):
            context['recent_reviews'] = guide.reviews.select_related(
                'traveler',
                'traveler__user'
            ).order_by('-created_at')[:5]
        else:
            context['recent_reviews'] = []
        
        context['guide'] = guide
        return context

class BookingListView(LoginRequiredMixin, ListView):
    model = GuideBooking
    template_name = 'local_guide/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        guide = get_object_or_404(LocalGuide, user=self.request.user)
        return GuideBooking.objects.filter(guide=guide).select_related(
            'traveler',
            'traveler__user'
        ).order_by('-created_at')

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = GuideBooking
    template_name = 'local_guide/booking_detail.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        guide = get_object_or_404(LocalGuide, user=self.request.user)
        return GuideBooking.objects.filter(guide=guide).select_related(
            'traveler',
            'traveler__user'
        )

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = GuideBooking
    fields = ['status']
    template_name = 'local_guide/booking_update.html'
    
    def get_queryset(self):
        guide = get_object_or_404(LocalGuide, user=self.request.user)
        return GuideBooking.objects.filter(guide=guide)
    
    def get_success_url(self):
        messages.success(self.request, 'Booking status updated successfully!')
        return reverse_lazy('local_guide:booking_list')

class PaymentListView(LoginRequiredMixin, ListView):
    template_name = 'local_guide/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 10
    
    def get_queryset(self):
        guide = get_object_or_404(LocalGuide, user=self.request.user)
        return GuideBooking.objects.filter(
            guide=guide,
            status__in=['confirmed', 'completed']
        ).select_related(
            'traveler',
            'traveler__user'
        ).order_by('-created_at')

class TravellerListView(LoginRequiredMixin, ListView):
    template_name = 'local_guide/traveller_list.html'
    context_object_name = 'travelers'
    paginate_by = 10
    
    def get_queryset(self):
        guide = get_object_or_404(LocalGuide, user=self.request.user)
        # Get all unique Traveler profiles who have booked this guide
        traveler_ids = GuideBooking.objects.filter(guide=guide).values_list('traveler', flat=True).distinct()
        from src.web.traveler.models import Traveler
        return Traveler.objects.filter(id__in=traveler_ids).select_related('user').order_by('-user__date_joined')

class TourListView(LoginRequiredMixin, ListView):
    template_name = 'local_guide/tour_list.html'
    context_object_name = 'tours'
    paginate_by = 10
    
    def get_queryset(self):
        guide = get_object_or_404(LocalGuide, user=self.request.user)
        return guide.tours.all().order_by('-created_at')

class SettingsView(LoginRequiredMixin, View):
    template_name = 'local_guide/settings.html'

    def get(self, request):
        guide = get_object_or_404(LocalGuide, user=request.user)
        context = {
            'guide': guide,
            'availability_choices': LocalGuide.AVAILABILITY_CHOICES,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        guide = get_object_or_404(LocalGuide, user=request.user)
        
        # Update basic info
        guide.full_name = request.POST.get('full_name', guide.full_name)
        guide.phone = request.POST.get('phone', guide.phone)
        guide.experience_years = request.POST.get('experience_years', guide.experience_years)
        guide.city = request.POST.get('city', guide.city)
        guide.country = request.POST.get('country', guide.country)
        guide.state = request.POST.get('state', guide.state)
        guide.zip_code = request.POST.get('zip_code', guide.zip_code)
        guide.address = request.POST.get('address', guide.address)
        guide.skills = request.POST.get('skills', guide.skills)
        guide.availability = request.POST.get('availability', guide.availability)

        # Handle profile image upload
        if 'image' in request.FILES:
            if guide.image:  # Delete old image if exists
                if os.path.isfile(guide.image.path):
                    os.remove(guide.image.path)
            guide.image = request.FILES['image']

        # Handle cover image upload
        if 'cover_image' in request.FILES:
            if guide.cover_image:  # Delete old cover image if exists
                if os.path.isfile(guide.cover_image.path):
                    os.remove(guide.cover_image.path)
            guide.cover_image = request.FILES['cover_image']

        try:
            guide.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')

        return redirect('local_guide:settings')

class LocalGuideListView(ListView):
    model = LocalGuide
    template_name = 'localguides/localguide_list.html'
    context_object_name = 'guides'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add any filtering/sorting here
        return queryset.select_related('user').prefetch_related('languages_spoken', 'certifications')

class LocalGuideCreateView(CreateView):
    model = LocalGuide
    form_class = LocalGuideForm
    template_name = 'localguides/localguide_form.html'
    success_url = reverse_lazy('localguide-list')
    
    def form_valid(self, form):
        # Set the user to the current logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

class LocalGuideDetailView(DetailView):
    model = LocalGuide
    template_name = 'localguides/localguide_detail.html'
    context_object_name = 'guide'
    
    def get_queryset(self):
        return super().get_queryset().select_related('user').prefetch_related(
            'languages_spoken__language',
            'certifications__certification'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['booking_form'] = GuideBookingForm(guide=self.object)
        return context

class BookGuideView(LoginRequiredMixin, CreateView):
    model = GuideBooking
    form_class = GuideBookingForm
    template_name = 'localguides/booking_form.html'
    
    def get_guide(self):
        return get_object_or_404(LocalGuide, pk=self.kwargs['guide_id'])
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['guide'] = self.get_guide()
        return kwargs
    
    def form_valid(self, form):
        guide = self.get_guide()
        booking = form.save(commit=False)
        booking.guide = guide
        booking.traveler = self.request.user.traveler
        booking.total_price = self.calculate_price(guide, form.cleaned_data)
        booking.save()
        messages.success(self.request, 'Your guide booking request has been submitted successfully!')
        return redirect('local_guide:booking-success', pk=booking.pk)
    
    def calculate_price(self, guide, cleaned_data):
        # Calculate price based on guide's rate and booking duration
        # This is a simple calculation - you might want to make it more complex
        days = (cleaned_data['end_date'] - cleaned_data['start_date']).days
        base_rate = 100  # You might want to store this in the guide model
        return base_rate * days * cleaned_data['number_of_people']

class BookingSuccessView(LoginRequiredMixin, DetailView):
    model = GuideBooking
    template_name = 'localguides/booking_success.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        return super().get_queryset().filter(traveler=self.request.user.traveler)