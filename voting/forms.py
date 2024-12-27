from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Poll, Option, Comment, Category

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category (optional)"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'category', 'password1', 'password2']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description', 'category', 'start_time', 'end_time', 
                 'is_public', 'allow_comments', 'multiple_choice']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text'] 