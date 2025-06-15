from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from src.accounts.forms import UserForm
from src.web.agency.models import Booking
from src.web.buyer.forms import BuyerPasswordChangeForm


class DashboardView(TemplateView):
    template_name = 'buyer/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = Booking.objects.filter(user=self.request.user)
        return context


class BookingView(TemplateView):
    Model = Booking
    template_name = 'buyer/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = Booking.objects.filter(user=self.request.user)
        return context


class PasswordChangeCustomView(View):
    template_name = 'buyer/password_change.html'

    def get(self, request):
        form = BuyerPasswordChangeForm(request.user)
        return render(request, self.template_name, context={'form': form})


def post(self, request):
    form = BuyerPasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Password Changed Successfully')
        return redirect('buyer:dashboard')
    else:
        messages.error(request, 'Error in Changing Password')
        return render(request, self.template_name, {'form': form})


class ProfileView(TemplateView):
    template_name = 'buyer/profile.html'


class ReviewsView(TemplateView):
    template_name = 'buyer/reviews.html'


class WishlistView(TemplateView):
    template_name = 'buyer/wishlist.html'


class SettingView(View):
    template_name = 'buyer/setting.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        form = UserForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            password = form.cleaned_data.get('current_password')
            print(password)
            form.save()
            return redirect('buyer:setting')
        else:
            print("errror")
            return render(request, self.template_name, {'form': form})
