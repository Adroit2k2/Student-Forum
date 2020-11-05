from django.contrib.auth.models import User
from django.views import View
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.core.paginator import Paginator
from django.db.models import Q
from home.utils import dump_queries
from django.http import HttpResponse
from django.db.models import F
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
from home.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
        # print("ANSHU_Chu?")
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        strval = request.GET.get("search", False)
        if strval:
            query = Q(topic__contains=strval)
            query.add(Q(description__contains=strval), Q.OR)
            objects = forum.objects.filter(query).select_related().order_by('-updated_at')
            p=1
        else:
            objects = forum.objects.all().order_by('-updated_at')
            p=0




        paginator = Paginator(objects, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        d=dict()
        for j in page_obj:
            try:
                vote, created = Vote.objects.get_or_create(userprofile=self.request.user,answer=j)
                d[j]=vote.votes

            except:
                pass


        dump_queries()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal,
            'forums' : page_obj,
            'available': p,
            'favorites': favorites,
            'Votes':d
        }

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
            context = {'form1': form1 ,'form2': form2,'form3': form3}


            return render(request, 'home/addInForum.html', context)
        forum = form1.save(commit=False)
        #form2.save(commit=False)



        for form in form3:
            form.save(commit=False)
        forum.owner = self.request.user
        forum.save()

        for form in form3:
            form.save(commit=False).option_access=forum
            form.save(commit=False).save()
        s=form2.cleaned_data.get('tags_forum')
        tags1=list(set(s.split(",")))
        tags=[]
        for j in tags1:
            tags.append(j.lstrip().rstrip())

        for j in tags:
            tag = forum_tags()
            tag.tags_forum = j
            tag.tags_access = forum
            tag.save()



        return redirect(reverse('home:content'))


class DeleteForum(LoginRequiredMixin, View):
    def get(self, request, pk) :
        forum.objects.filter(pk=pk).delete()
        return HttpResponse()


    def post(self, request, pk) :
        forum.objects.filter(pk=pk).delete()
        return HttpResponse()








class ForumUpdate(LoginRequiredMixin, View):
    template_name = 'home/updateForum.html'
    success_url = reverse_lazy('home:content')
    def get(self, request, pk) :
        forum1 = get_object_or_404(forum, id=pk, owner=self.request.user)
        form = CreateInForum(instance=forum1)
        ctx = { 'form': form }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None) :
        forum1 = get_object_or_404(forum, id=pk, owner=self.request.user)
        form = CreateInForum(request.POST or None, instance=forum1)

        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, self.template_name, ctx)

        forum1 = form.save(commit=False)
        forum1.save()

        return redirect(self.success_url)


class addInDiscussion(LoginRequiredMixin, View):
    form = CreateInDiscussion()
    def get(self,request, pk):
        form =  CreateInDiscussion()
        topic=forum.objects.get(pk=pk)

        context = { 'form': form, 'pk': pk,'topic':topic, }
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
        return redirect(reverse('home:content'))



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
    forums=forum.objects.all()
    return render(request = request,
                    template_name = "home/login.html",
                    context={"form":form,"forums":forums})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/home")




class UsersView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        strval = request.GET.get("search", False)
        if strval:
            query = Q(username__contains=strval)
            objects = User.objects.filter(query).select_related().order_by('-date_joined')[:10]
            p=1
        else:
            objects = User.objects.all().order_by('-date_joined')[:15]
            p=0

        paginator = Paginator(objects, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal,
            'users' : page_obj,
            'available': p
        }
        dump_queries()
        return render(request, 'home/users.html', context)


class TagsView(View):
    def get(self, request) :
        print(request.get_host())
        host = request.get_host()
        islocal = host.find('localhost') >= 0 or host.find('127.0.0.1') >= 0
        strval = request.GET.get("search", False)
        if strval:
            query = Q(tags_forum__contains=strval)
            objects = forum_tags.objects.filter(query).select_related().order_by('-tags_forum')
            p=1
        else:
            objects = forum_tags.objects.all().order_by('-tags_forum')
            p=0



        context = {
            'installed' : settings.INSTALLED_APPS,
            'islocal' : islocal,
            'available': p
        }
        a=[]
        for tag in objects:
            if tag.tags_forum!="":
                a.append(tag.tags_forum)
        a=list(set(a))
        paginator = Paginator(a, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['tags']=page_obj

        dump_queries()
        return render(request, 'home/searchtags.html', context)


class ForumTagsView(View):
    def get(self,request,pk):
        tags = forum_tags.objects.filter(tags_forum=pk)

        return render(request, 'home/TagsForum.html', {'tags': tags})


class ProfileSearchView(View):
    def get(self,request,pk):
        prof=User.objects.get(username=pk)
        objects = forum.objects.filter(owner=prof.id).order_by('-updated_at')[:15]
        form = CreateLink()
        form2=CreateBio()
        context = {'prof':prof,'forums':objects,'form':form,'form2':form2}

        return render(request, 'home/searchprofile.html', context)

    def post(self,request,pk):
        form = CreateLink(request.POST)
        form2 = CreateBio(request.POST)

        if form.is_valid():
            linkedin_link=""
            github_link=""
            linkedin_link = form.cleaned_data.get('linkedin_link')
            github_link = form.cleaned_data.get('github_link')
            bio=form2.cleaned_data.get('bio')
            user=User.objects.get(username=pk)
            user.profile.linkedin_link= linkedin_link
            user.profile.github_link= github_link
            user.profile.bio=bio

            user.save()

            return redirect(reverse('home:searchprofile', kwargs={'pk':pk}))

        if form2.is_valid():
            bio=form2.cleaned_data.get('bio')
            user=User.objects.get(username=pk)

            user.profile.bio=bio

            user.save()

            return redirect(reverse('home:searchprofile', kwargs={'pk':pk}))

        prof=User.objects.get(username=pk)
        #user=User.objects.get(username=pk)
        #user.profile.linkedin_link= "http://www.blankwebsite.com/"
        #user.profile.github_link= github_link="http://www.blankwebsite.com/"

        #user.save()
        objects = forum.objects.filter(owner=prof.id).order_by('-updated_at')[:15]
        form = CreateLink()
        context = {'prof':prof,'forums':objects,'form':form}
        return render(request, 'home/searchprofile.html', context)





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

class Change_password(OwnerUpdateView):

    def get(self,request):
        form = PasswordChangeForm(request.user)
        return render(request, 'home/change_password.html', {'form': form})

    def post(self,request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home:content')
        else:
            messages.error(request, 'Please correct the error below.')





class addInUpVote(LoginRequiredMixin, APIView):
    #form = CreateInDiscussion()
    #def get(self,request, pk):
    #   form =  CreateInDiscussion()
    #    context = { 'form': form, 'pk': pk }
    #    return render(request, 'forums/addInDiscussion.html', context)


    def post(self,request, pk):
        b=forum.objects.get(pk=pk)
        vote, created = Vote.objects.get_or_create(userprofile=self.request.user,answer=b)
        if vote.votes==0:
            vote.votes=1
            b.total+=1
        elif vote.votes==-1:
            vote.votes=1
            b.total+=2
        elif vote.votes==1:
            vote.votes=0
            b.total-=1

        vote.save()
        b.save()
        # return redirect('home:content')
        return Response({"total": b.total,"vote":vote.votes}, status=200)


class addInDownVote(LoginRequiredMixin, APIView):
    #form = CreateInDiscussion()
    #def get(self,request, pk):
    #   form =  CreateInDiscussion()
    #    context = { 'form': form, 'pk': pk }
    #    return render(request, 'forums/addInDiscussion.html', context)


    def post(self,request, pk):
        b=forum.objects.get(pk=pk)
        vote, created = Vote.objects.get_or_create(userprofile=self.request.user,answer=b)
        if vote.votes==0:
            vote.votes=-1
            b.total-=1
        elif vote.votes==1:
            vote.votes=-1
            b.total-=2
        elif vote.votes==-1:
            vote.votes=0
            b.total+=1

        vote.save()
        b.save()
        # return redirect('home:content')
        return Response({"total": b.total,"vote":vote.votes}, status=200)



from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        t = get_object_or_404(forum, id=pk)
        fav = Fav(user=request.user, forum_fav=t)
        try:
            fav.save()
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(forum, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, forum_fav=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()

