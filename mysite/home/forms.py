from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import formset_factory
from home.humanize import naturalsize

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    phone = forms.DecimalField(max_digits=10, help_text='Phone number')

    def get_context_data(self, **kwargs):
        ctx = super(SignUpForm, self).get_context_data(**kwargs)
        ctx['user'] = User.objects.all()[0]
        return ctx


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email', 'password1', 'password2','phone')




class EditProfileForm(ModelForm):

    max_upload_limit = 2 * 1024 * 1024
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name','email','phone','picture')


    def clean(self) :
        cleaned_data = super().clean()
        prof = cleaned_data.get('picture')
        if prof is None : return
        if len(prof) > self.max_upload_limit:
            self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True) :
        instance = super(EditProfileForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read();
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        #else:
            #return instance

        if commit:
            instance.save()

        return instance

# class TagWidget(forms.MultiWidget):
#     def __init__(self, *args, **kwargs):
#         super(PhoneNumberWidget, self).__init__(*args, **kwargs)
#         self.widgets = [
#             forms.TextInput(),
#             forms.TextInput(),
#             forms.TextInput(),
#             forms.TextInput(),
#             forms.TextInput(),
#         ]
#     def decompress(self, value):
#         if value:
#             return value.split(' ')
#         return [None, None]

# class TagsField(forms.MultiValueField):
#     widget = PhoneNumberWidget

#     def __init__(self, *args, **kwargs):
#         super(PhoneNumberField, self).__init__(*args, **kwargs)
#         fields = (
#             forms.CharField(),
#             forms.CharField()
#         )

#     def compress(self, data_list):
#         return ' '.join(data_list)

class CreateInForum(ModelForm):
    class Meta:
        model = forum
        fields = ['topic', 'description', 'type_code','ask']



class CreateTag(ModelForm):

    class Meta:
        model = forum_tags
        fields = ['tags_forum']

class CreateLink(ModelForm):
    linkedin_link = forms.URLField(max_length=200, help_text='linkedin_link')
    github_link = forms.URLField(max_length=100, help_text='github_link')

    class Meta:
        model = Profile
        fields = ['linkedin_link','github_link']

class CreateBio(ModelForm):
    bio = forms.CharField(max_length=200, help_text='bio')

    class Meta:
        model = Profile
        fields = ['bio']






class CreateOptions(ModelForm):
    class Meta:
        model = options
        fields = ['option']
CreateOptionsFormSet = formset_factory(CreateOptions, extra = 4)


class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = ['discuss','single']




