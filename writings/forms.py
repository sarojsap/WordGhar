from django import forms
from .models import Writing

class WritingForm(forms.ModelForm):
    class Meta:
        model = Writing
        fields = ['title', 'category', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'शीर्षक (Title)'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2 h-64 focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'यहाँ लेख्नुहोस्...'
            }),
        }