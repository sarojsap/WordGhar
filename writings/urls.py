from django.urls import path
from .views import WritingListView, WritingDetailView, WritingCreateView

urlpatterns = [
    path('', WritingListView.as_view(), name='writing_list'),
    path('new/', WritingCreateView.as_view(), name='writing_create'),
    path('read/<str:slug>/', WritingDetailView.as_view(), name='writing_detail')
]
