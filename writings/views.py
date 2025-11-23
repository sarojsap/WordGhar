from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Writing
from .forms import WritingForm

class WritingListView(ListView):
    model = Writing
    context_object_name = 'writings'
    template_name = 'writings/writing_list.html'

    # If you later add a `published` boolean field, replace this with:
    # return Writing.objects.filter(published=True)

    def get_queryset(self):
        return Writing.objects.all().order_by('-created_at')
    
class WritingDetailView(DetailView):
    model = Writing
    context_object_name = 'writing'
    template_name = 'writings/writing_detail.html'

class WritingCreateView(LoginRequiredMixin, CreateView):
    model = Writing
    form_class = WritingForm
    template_name = 'writings/writing_form.html'

    success_url = reverse_lazy('writing_list') 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)