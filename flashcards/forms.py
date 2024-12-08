from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db import models
from .models import Collection, FlashCard, Comment

# Use the custom User model
User = get_user_model()


# Custom User Creation Form
class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating new users with additional email field and placeholder attributes.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        label="Email Address"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter a password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }


# Collection Form
class CollectionForm(forms.ModelForm):
    """
    Form for creating or editing collections.
    Allows users to select flashcards from their own or shared collections.
    """
    flashcards = forms.ModelMultipleChoiceField(
        queryset=FlashCard.objects.none(),  # Initially empty, populated dynamically
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Flashcards"
    )
    class Meta:
        model = Collection
        fields = ['name', 'flashcards']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter collection name'}),
        }
        labels = {
            'name': "Collection Name",
            'flashcards': "Flashcards in Collection",
        }
    def __init__(self, *args, **kwargs):
        """
        Initializes the form and populates the flashcard queryset based on the user.
        """
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        if user:
            
            self.fields['flashcards'].queryset = FlashCard.objects.filter(
                models.Q(created_by=user) | models.Q(is_shared=True)
            )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
            }),
        }

# FlashCard Form
class FlashCardForm(forms.ModelForm):
    """
    Form for creating or editing flashcards.
    Includes fields for question, answer, and difficulty.
    """
    class Meta:
        model = FlashCard
        fields = ['question', 'answer', 'difficulty']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your question'
            }),
            'answer': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter the answer'
            }),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
        }



