from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import LocalGuide, GuideBooking
from .forms import LocalGuideForm, GuideBookingForm

class LocalGuideDashboardView(TemplateView):
    template_name = 'local_guide/dashboard.html'
    


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