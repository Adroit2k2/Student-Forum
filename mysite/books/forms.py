from django import forms
from django.forms import ModelForm
from .models import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import formset_factory


class AddinCart(ModelForm):
    code = forms.CharField(max_length=100)

    class Meta:
        model = AddInCart
        fields = ['user','code']