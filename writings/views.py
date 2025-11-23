from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Writing
from .forms import WritingForm

class WritingListView(ListView):
    model = Writing
    context_object_name = 'writings'
    template_name = 'writings/writing_list.html'

    # If you later add a `published` boolean field, replace this with:
    # return Writing.objects.filter(published=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get filter parameters from URL
        query = self.request.GET.get('q')
        category_filter = self.request.GET.get('category')  # poem or story
        content_category_filter = self.request.GET.get('content_category')  # content category
        
        # Filter by poem/story category
        if category_filter in ['poem', 'story']:
            queryset = queryset.filter(category=category_filter)
        
        # Filter by content category
        if content_category_filter:
            queryset = queryset.filter(content_category=content_category_filter)
        
        # Search filter
        if query:
            # Filter: Title contains query OR Content contains query
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_content_category'] = self.request.GET.get('content_category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
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
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)

class WritingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Writing
    form_class = WritingForm
    template_name = 'writings/writing_form.html'
    context_object_name = 'writing'

    def test_func(self):
        writing = self.get_object()
        return writing.author == self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Your post has been updated successfully!')
        return reverse_lazy('writing_detail', kwargs={'slug': self.object.slug})

class WritingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Writing
    template_name = 'writings/writing_confirm_delete.html'
    context_object_name = 'writing'
    success_url = reverse_lazy('writing_list')

    def test_func(self):
        writing = self.get_object()
        return writing.author == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

class MyPostsView(LoginRequiredMixin, ListView):
    model = Writing
    context_object_name = 'writings'
    template_name = 'writings/my_posts.html'

    def get_queryset(self):
        return Writing.objects.filter(author=self.request.user).order_by('-created_at')