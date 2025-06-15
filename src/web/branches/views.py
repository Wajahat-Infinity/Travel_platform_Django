from django.views import View
from django.views.generic import TemplateView

from src.accounts.forms import IncompleteBranchForm

from django.shortcuts import render, get_object_or_404

from src.web.agency.models import Branch


class DashboardView(TemplateView):
    template_name = 'branches/dashboard.html'


class BookingView(TemplateView):
    template_name = 'branches/booking.html'


class ProfileView(TemplateView):
    template_name = 'branches/profile.html'


class ProfileEditView(View):
    template_name = 'branches/edit_profile.html'
    form = IncompleteBranchForm

    def get(self, request):
        user = request.user
        branch_instance = get_object_or_404(Branch, branch_manager=user)
        form = self.form(instance=branch_instance)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        branch_instance = get_object_or_404(Branch, branch_manager=user)
        form = self.form(request.POST, request.Files, instance=branch_instance)
        if form.is_valid():
            form.save()
            context = {
                'form': form
            }
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {'form': form})


class ReviewsView(TemplateView):
    template_name = 'branches/reviews.html'


class SettingView(TemplateView):
    template_name = 'branches/setting.html'
