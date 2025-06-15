from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from src.accounts.forms import IncompleteAgencyForm, UserForm, IncompleteBranchForm, VehicleForm
from src.web.agency.models import Booking, Branch, Agency, Vehicle

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'agency/dashboard.html'


@method_decorator(login_required, name='dispatch')
class BookingView(ListView):
    model = Booking
    template_name = 'agency/booking.html'
    context_object_name = 'bookings'


@method_decorator(login_required, name='dispatch')
class BranchesView(TemplateView):
    template_name = 'agency/branches.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branches'] = Branch.objects.filter(agency__owner=self.request.user)
        return context


class BranchesAddView(CreateView):
    model = Branch
    form_class = IncompleteBranchForm
    template_name = 'agency/add_branch.html'
    success_url = reverse_lazy('agency:branches')

    def form_valid(self, form):
        branch = form.save(commit=False)
        branch.agency = Agency.objects.get(owner=self.request.user)
        branch.branch_manager = self.request.user
        branch.save()

        messages.success(self.request, 'Branch Added Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error adding branch')
        return self.render_to_response(self.get_context_data(form=form))


class BranchesUpdateView(UpdateView):
    model = Branch
    form_class = IncompleteBranchForm
    template_name = 'agency/add_branch.html'
    success_url = reverse_lazy('agency:branches')

    def form_valid(self, form):
        branch = form.save(commit=False)
        branch.agency = Agency.objects.get(owner=self.request.user)
        branch.branch_manager = self.request.user
        branch.save()

        messages.success(self.request, 'Branch Added Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(self.request, 'Error adding branch')
        return self.render_to_response(self.get_context_data(form=form))


class BranchesDeleteView(View):
    def get(self, request, id):
        branch = get_object_or_404(Branch, id=id)
        branch.delete()
        return redirect('agency:branches')


@method_decorator(login_required, name='dispatch')
class VehicleView(TemplateView):
    template_name = 'agency/vehicle.html'


class VehicleCreateView(CreateView):
    model = Vehicle
    form_class = VehicleForm


@method_decorator(login_required, name='dispatch')
class OrdersView(TemplateView):
    template_name = 'agency/orders.html'


@method_decorator(login_required, name='dispatch')
class TravellersView(TemplateView):
    template_name = 'agency/travellers.html'


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'agency/profile.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    template_name = 'agency/edit_profile.html'
    form_class = IncompleteAgencyForm

    def get(self, request):
        user = request.user
        agency_instance = get_object_or_404(Agency, owner=user)
        form = self.form_class(instance=agency_instance)
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request):
        user = request.user
        agency_instance = get_object_or_404(Agency, owner=user)
        form = self.form_class(request.POST, request.FILES, instance=agency_instance)
        if form.is_valid():
            form.save()
            return render(request, template_name=self.template_name, context={"form": form})
        else:
            return render(request, template_name=self.template_name, context={"form": form})


@method_decorator(login_required, name='dispatch')
class ReviewsView(TemplateView):
    template_name = 'agency/reviews.html'


@method_decorator(login_required, name='dispatch')
class WishlistView(TemplateView):
    template_name = 'agency/wishlist.html'


@method_decorator(login_required, name='dispatch')
class TravelAgentsView(TemplateView):
    template_name = 'agency/travel_agents.html'


@method_decorator(login_required, name='dispatch')
class InvoicesView(TemplateView):
    template_name = 'agency/invoices.html'


@method_decorator(login_required, name='dispatch')
class PaymentsView(TemplateView):
    template_name = 'agency/payments.html'


@method_decorator(login_required, name='dispatch')
class CurrencyView(TemplateView):
    template_name = 'agency/currency.html'


@method_decorator(login_required, name='dispatch')
class SubscriberView(TemplateView):
    template_name = 'agency/subscriber.html'


@method_decorator(login_required, name='dispatch')
class LocationView(TemplateView):
    template_name = 'agency/location.html'


@method_decorator(login_required, name='dispatch')
class SettingView(View):
    template_name = 'agency/setting.html'
    form = UserForm

    def get(self, request):
        form = self.form(instance=request.user)
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request):
        form = self.form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Updated Successfully')
            return redirect('agency:setting')
        else:
            messages.error(request, "Error While Updating")
            return render(request, template_name=self.template_name, context={"form": form})
