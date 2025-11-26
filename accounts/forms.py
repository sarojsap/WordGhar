from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
            'placeholder': 'First Name (पहिलो नाम)',
            'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
            'placeholder': 'Last Name (अन्तिम नाम)',
            'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
        })
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
            'type': 'date',
            'placeholder': 'Date of Birth (जन्म मिति)',
            'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
            'placeholder': 'Password',
            'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
            'placeholder': 'Confirm Password',
            'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide password help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'placeholder': 'Username',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('bio', 'profile_photo', 'first_name', 'last_name')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'rows': 4,
                'placeholder': 'Write a short bio about yourself...',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'placeholder': 'First Name (पहिलो नाम)',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'placeholder': 'Last Name (अन्तिम नाम)',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 theme-bg-secondary theme-border theme-text-primary border rounded-lg focus:outline-none focus:ring-2 focus:ring-lavender-500 transition',
                'accept': 'image/*',
                'style': 'background-color: var(--bg-secondary); color: var(--text-primary); border-color: var(--border-color);'
            }),
        }