from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from writings.models import Writing
from .forms import CustomUserCreationForm, ProfileEditForm

User = get_user_model()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['writings'] = Writing.objects.filter(author=self.object).order_by('-created_at')
        context['is_own_profile'] = self.object == self.request.user
        return context

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        messages.success(self.request, 'Your profile has been updated successfully!')
        return reverse_lazy('profile', kwargs={'username': self.object.username})

class AuthorProfileView(LoginRequiredMixin, DetailView):
    """View to see any author's profile"""
    model = User
    template_name = 'accounts/author_profile.html'
    context_object_name = 'author'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['writings'] = Writing.objects.filter(author=self.object).order_by('-created_at')
        return context