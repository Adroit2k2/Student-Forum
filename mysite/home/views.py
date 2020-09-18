
from django.views import View
from django.conf import settings
from django.contrib.auth import login, authenticate, logout

from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


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
        forums = forum.objects.all()
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal,
            'forums' : forums
        }
        return render(request, 'home/content.html', context)

class addInForum(LoginRequiredMixin, View):
    def get(self,request,pk=None):
        form = CreateInForum()
        forums = forum.objects.all()
        context = { 'form': form ,'forums':forums}
        return render(request, 'home/addInForum.html', context)

    def post(self,request):
        form = CreateInForum(request.POST)
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'home/addInForum.html', context)
        forum = form.save(commit=False)
        forum.owner = self.request.user
        forum.save()




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
        return redirect(reverse_lazy('home:content'))



class addInTag(LoginRequiredMixin, View):

    def get(self,request, pk):
        form =  CreateTag()
        forums = forum.objects.all()
        context = { 'forums': forums,'pk': pk, 'form': form }
        return render(request, 'home/addInTag.html', context)


    def post(self,request, pk):
        form = CreateTag(request.POST)
        if not form.is_valid():
            context = {'form': form, 'pk': pk}
            return render(request, 'home/addInTag.html', context)

        tag = form.save(commit=False)
        tag.tags_access=forum.objects.get(pk=pk)
        tag.save()
        return redirect(reverse_lazy('home:content'))

def signup_view(request):

    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.save()
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
                return redirect('/home')
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



