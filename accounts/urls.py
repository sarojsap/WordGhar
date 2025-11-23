from django.urls import path
from .views import SignUpView, ProfileView, ProfileEditView, AuthorProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('author/<str:username>/', AuthorProfileView.as_view(), name='author_profile'),
]
