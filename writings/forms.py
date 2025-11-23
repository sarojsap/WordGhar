from django import forms
from .models import Writing, ContentCategory

class WritingForm(forms.ModelForm):
    class Meta:
        model = Writing
        fields = ['title', 'category', 'content_category', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full theme-bg-secondary theme-border theme-text-primary border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'placeholder': 'शीर्षक (Title)',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full theme-bg-secondary theme-border theme-text-primary border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
            'content_category': forms.Select(attrs={
                'class': 'w-full theme-bg-secondary theme-border theme-text-primary border rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full theme-bg-secondary theme-border theme-text-primary border rounded-lg px-4 py-3 h-64 focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'placeholder': 'यहाँ लेख्नुहोस्...',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
        }