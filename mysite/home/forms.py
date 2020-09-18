from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    def get_context_data(self, **kwargs):
        ctx = super(SignUpForm, self).get_context_data(**kwargs)
        ctx['user'] = User.objects.all()[0]
        return ctx


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2',)

class CreateInForum(ModelForm):
    class Meta:
        model = forum
        fields = ['topic', 'description']

class CreateTag(ModelForm):
    class Meta:
        model = forum_tags
        fields = ['tags_forum']

class CreateOptions(ModelForm):
    class Meta:
        model = options
        fields = ['option']



class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = ['discuss']