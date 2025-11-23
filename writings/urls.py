from django.urls import path
from .views import WritingListView, WritingDetailView, WritingCreateView, WritingUpdateView, WritingDeleteView, MyPostsView

urlpatterns = [
    path('', WritingListView.as_view(), name='writing_list'),
    path('new/', WritingCreateView.as_view(), name='writing_create'),
    path('read/<str:slug>/', WritingDetailView.as_view(), name='writing_detail'),
    path('edit/<str:slug>/', WritingUpdateView.as_view(), name='writing_update'),
    path('delete/<str:slug>/', WritingDeleteView.as_view(), name='writing_delete'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
]
