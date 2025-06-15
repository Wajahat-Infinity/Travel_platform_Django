from django.views.generic import TemplateView

class AgencyDashboardView(TemplateView):
    template_name = 'agency/dashboard.html'