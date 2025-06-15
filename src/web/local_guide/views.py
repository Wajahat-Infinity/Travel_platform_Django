from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import LocalGuide
from .forms import LocalGuideForm

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