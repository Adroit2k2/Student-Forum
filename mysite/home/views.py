import os
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.views import View
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from home.utils import dump_queries
from django.http import HttpResponse

from .forms import SignUpForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
class HomeView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal
        }
        return render(request, 'home/base.html', context)

class ContentView(View):
    def get(self, request) :
        # print("ANSHU")
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        strval = request.GET.get("search", False)
        if strval:
            query = Q(topic__contains=strval)
            query.add(Q(description__contains=strval), Q.OR)
            objects = forum.objects.filter(query).select_related().order_by('-date_created')[:10]
            p=1
        else:
            objects = forum.objects.all().order_by('-date_created')[:15]
            p=0
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal,
            'forums' : objects,
            'available': p
        }
        dump_queries()
        return render(request, 'home/content.html', context)

class addInForum(LoginRequiredMixin, View):

    def get(self,request,pk=None):
        form1 = CreateInForum()
        form2 = CreateTag()

        form3 = CreateOptionsFormSet()
        forums = forum.objects.all()

        context = { 'form1': form1 ,'form2': form2 ,'form3': form3 ,'forums':forums}
        return render(request, 'home/addInForum.html', context)

    def post(self,request):
        form1 = CreateInForum(request.POST)
        form2 = CreateTag(request.POST)

        form3 = CreateOptionsFormSet(request.POST)
        if not (form1.is_valid() and form2.is_valid() and form3.is_valid()):
            context = {'form1': form1 ,'form2': form2,'form2': form2}


            return render(request, 'home/addInForum.html', context)
        forum = form1.save(commit=False)
        tag = form2.save(commit=False)
        for form in form3:
            form.save(commit=False)
        forum.owner = self.request.user
        forum.save()

        for form in form3:
            form.save(commit=False).option_access=forum
            form.save(commit=False).save()

        tag.tags_access=forum

        tag.save()

        return redirect(reverse('home:content'))




class addInDiscussion(LoginRequiredMixin, View):
    form = CreateInDiscussion()
    def get(self,request, pk):
        form =  CreateInDiscussion()
        context = { 'form': form, 'pk': pk }
        return render(request, 'home/addInDiscussion.html', context)


    def post(self,request, pk):
        form = CreateInDiscussion(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'home/addInDiscussion.html', context)

        discussion = form.save(commit=False)
        discussion.creator = self.request.user
        discussion.forum= get_object_or_404(forum, id=pk)
        discussion.save()
        return redirect(reverse('home:option', kwargs={'pk':pk}))



class addInTag(LoginRequiredMixin, View):

    def get(self,request, pk):
        form =  CreateTag()
        forums = forum.objects.all()
        viewtags=forum.objects.get(pk=pk)
        context = { 'forums': forums,'pk': pk, 'form': form, 'viewtags':viewtags }
        return render(request, 'home/addInTag.html', context)


    def post(self,request, pk):
        form = CreateTag(request.POST)
        if not form.is_valid():
            viewtags=forum.objects.get(pk=pk)
            context = {'form': form, 'pk': pk, 'viewtags':viewtags}
            return render(request, 'home/addInTag.html', context)

        tag = form.save(commit=False)
        tag.tags_access=forum.objects.get(pk=pk)
        tag.save()
        if 'Add' in self.request.POST:
            return redirect(reverse('home:tags', kwargs={'pk':pk}))
        else:
            return redirect(reverse('home:content'))




class addInOption(LoginRequiredMixin, View):

    def get(self,request, pk):
        form =  CreateOptions()
        forums = forum.objects.all()
        context = { 'forums': forums,'pk': pk, 'form': form }
        return render(request, 'home/addInOption.html', context)


    def post(self,request, pk):
        form = CreateOptions(request.POST)
        if not form.is_valid():
            context = {'form': form, 'pk': pk}
            return render(request, 'home/addInOption.html', context)

        option = form.save(commit=False)
        option.option_access=forum.objects.get(pk=pk)
        option.save()
        if 'Add' in self.request.POST:
            return redirect(reverse('home:option', kwargs={'pk':pk}))
        else:
            return redirect(reverse('home:tags', kwargs={'pk':pk}))




def signup_view(request):

    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone = form.cleaned_data.get('phone')
            user.save()

            #message = Mail(
            #    from_email='vbhadola92@gmail.com',
            #    to_emails=user.profile.email,
            #    subject='Sending with Twilio SendGrid is Fun',
            #    html_content='<strong>and easy to do anywhere, even with Python</strong>')
            # try:
            #sg = SendGridAPIClient(os.environ.['SENDGRID_API_KEY'])
            #response = sg.send(message)
            #print(response.status_code)
            #print(response.body)
            #print(response.headers)

            # except Exception as e:
            #     print(e.message)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/home')

    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as vivek {username}")
                return redirect('home:content')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "home/login.html",
                    context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/home")


class ProfileView(LoginRequiredMixin, View):
    def get(self,request):
        context = {}
        return render(request, 'home/profile.html', context)

class EditProfile(LoginRequiredMixin, View):
    def get(self,request,pk):
        prof=get_object_or_404(Profile, id=pk, user=self.request.user)
        form = EditProfileForm(instance=prof)

        return render(request, 'home/editprofile.html', {'form': form})




    def post(self,request,pk):
        prof=get_object_or_404(Profile, id=pk, user=self.request.user)
        form = EditProfileForm(request.POST, request.FILES or None,instance=prof)
        if form.is_valid():

            profile = form.save(commit=False)
            profile.save()
            return redirect('/home')

        else:

            return render(request, 'home/editprofile.html', {'form': form})


def stream_file(request, pk) :
    profile = get_object_or_404(Profile, id=pk)
    response = HttpResponse()
    response['Content-Type'] = profile.content_type
    response['Content-Length'] = len(profile.picture)
    response.write(profile.picture)
    return response

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home:content')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/change_password.html', {'form': form})


