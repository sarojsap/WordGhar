from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Writing, Like, Comment
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        writing = self.object
        
        # Get like count and check if current user liked it
        context['like_count'] = writing.get_like_count()
        if self.request.user.is_authenticated:
            context['is_liked'] = writing.is_liked_by(self.request.user)
        else:
            context['is_liked'] = False
        
        # Get all comments
        context['comments'] = writing.comments.all()
        
        return context

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


@login_required
@require_POST
def toggle_like(request, slug):
    """Toggle like on a writing"""
    writing = get_object_or_404(Writing, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, writing=writing)
    
    if not created:
        # Unlike - delete the like
        like.delete()
        is_liked = False
    else:
        # Like - already created
        is_liked = True
    
    like_count = writing.get_like_count()
    
    return JsonResponse({
        'is_liked': is_liked,
        'like_count': like_count
    })


@login_required
@require_POST
def add_comment(request, slug):
    """Add a comment to a writing"""
    writing = get_object_or_404(Writing, slug=slug)
    content = request.POST.get('content', '').strip()
    
    if not content:
        messages.error(request, 'Comment cannot be empty.')
        return redirect('writing_detail', slug=slug)
    
    if len(content) > 1000:
        messages.error(request, 'Comment is too long. Maximum 1000 characters.')
        return redirect('writing_detail', slug=slug)
    
    Comment.objects.create(
        writing=writing,
        user=request.user,
        content=content
    )
    
    messages.success(request, 'Comment added successfully!')
    return redirect('writing_detail', slug=slug)


@login_required
@require_POST
def delete_comment(request, comment_id):
    """Delete a comment - only author or post author can delete"""
    comment = get_object_or_404(Comment, id=comment_id)
    writing = comment.writing
    
    # Check if user is comment author or writing author
    if request.user != comment.user and request.user != writing.author:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect('writing_detail', slug=writing.slug)
    
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('writing_detail', slug=writing.slug)