from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import requests
import json
from .services import *
from django.core.paginator import Paginator
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse

def search(View):
    return render(View, 'books/search.html')


#Search_Result Page


def api(request):
    # query = request.GET
    searchterms={}
    querystring=""
    if request.method == 'POST':
        searchterms["intitle"] = request.POST['name']
        searchterms['inauthor'] = request.POST['author']
        searchterms['inpublisher'] = request.POST['publisher']
        general=request.POST['isbn']

    arr = []
    try:
        querystring += str(general)
        for f in searchterms:
            if len(searchterms[f]):
                querystring += ("+" if len(querystring) else "") + f + ':' + searchterms[f]
        searchterms['general']=general
        googleapikey = "AIzaSyDragr-Pcph1OpaIGSvXlw-xwHsu3FLRXY"
        bookshelf = []
        params = {'q': querystring, 'key': googleapikey , 'maxResults':30}
        google_books = requests.get(url="https://www.googleapis.com/books/v1/volumes/", params=params)
        books_json = google_books.json()
        for each in books_json['items']:
            bookshelf.append(each)

        for book in bookshelf:
            d={}
            for each in ['title', 'authors', 'description']:
                try:
                    d[each] = book['volumeInfo'][each]
                except:
                    d[each] = "No Description"
            try:
                d["imagelink"]= str(book["volumeInfo"]["imageLinks"]["thumbnail"])
            except:
                d['imagelink']= "https://safetyaustraliagroup.com.au/wp-content/uploads/2019/05/image-not-found.png"

            d['viewable'] = str(book['accessInfo']['embeddable'])

            d['id']=book['id']

            d['authors']=str(d['authors'])[1:-1]
            lst_auth=d['authors'].split(',')
            fnl_lst_auth = []
            fnl_lst_auth.append(lst_auth[0][1:-1])
            for each in lst_auth[1:]:
                fnl_lst_auth.append(each[2:-1])
            d['authors']=", ".join(fnl_lst_auth)
            if d['authors'] == 'Descripti':
                d['authors']='Author Not Found'
            arr.append(d)
            books=1
    except:
        books=0

    content = {'books': books,
               'bookshelf': arr,
               'searchterm':searchterms}
    return render(request, 'books/api.html' , content)
    # return render(request, 'books/api.html', response)



#Final Page

@login_required
def result(request , val):
    if request.method == 'POST':
        code = request.POST['code']
    else:
        code=val
    d = {}
    form=get_add(request,code)
    querystring = str(str(code))
    googleapikey = "AIzaSyDragr-Pcph1OpaIGSvXlw-xwHsu3FLRXY"
    url_search = "https://www.googleapis.com/books/v1/volumes/" + str(querystring) +"?key=" + str(googleapikey) + "&country=IN"
    google_books = requests.get(url=url_search)
    books_json = google_books.json()
    book = books_json
    for each in ['title', 'authors', 'description','categories','averageRating']:
        try:
            d[each] = book['volumeInfo'][each]
        except:
            d[each] = "No Description"
    try:
        d["imagelink"]= str(book["volumeInfo"]["imageLinks"]["thumbnail"])
    except:
        d['imagelink']= "https://safetyaustraliagroup.com.au/wp-content/uploads/2019/05/image-not-found.png"
    try:
        d['pdf'] = book['accessInfo']['pdf']['isAvailable']

        if d['pdf'] :
            try:
                d['dwnld_link_p']=book['accessInfo']['pdf']['downloadLink']
            except:
                d['pdf']= False
    except:
        d['pdf'] = 'not available'

    try:
        d['epub'] = book['accessInfo']['epub']['isAvailable']
        if d['epub'] :
            try:
                d['dwnld_link_e'] = book['accessInfo']['epub']['downloadLink']
            except:
                d['epub']=False
    except:
        d['epub'] = 'not available'
    saleable=0
    try:
        d['list_price']= str(book['saleInfo']['listPrice'][1]) +" "+ str(book['saleInfo']['listPrice'][0])
        d['re_price']= str(book['saleInfo']['retailPrice'][1]) +" "+ str(book['saleInfo']['retailPrice'][0])
        d['buylink']=str(book['saleInfo']['buyLink'])
        saleable=1
    except:
        saleable=0
    d['id']=book['id']
    d['authors']=str(d['authors'])[1:-1]
    lst_auth=d['authors'].split(',')
    fnl_lst_auth = []
    fnl_lst_auth.append(lst_auth[0][1:-1])
    for each in lst_auth[1:]:
        fnl_lst_auth.append(each[2:-1])
    d['authors']=", ".join(fnl_lst_auth)
    d['categories']=str(d['categories'])[1:-1]
    lst_cat=d['categories'].split(',')
    fnl_lst_cat = []
    fnl_lst_cat.append(lst_cat[0][1:-1])
    for each in lst_cat[1:]:
        fnl_lst_cat.append(each[2:-1])
    d['categories']=", ".join(fnl_lst_cat)
    redirect_query = 'https://b-ok.asia/s/?q=' + str(d['title']) + '%2C' + str("+".join(d['authors'].split(" ")))
    if d['authors'] == 'Descripti':
        d['authors']='Author Not Found'
        redirect_query = 'https://b-ok.asia/s/?q=' + str(d['title']) + '%2C'
    d['categories']=d['categories'].strip()
    if d['categories'] == 'Descripti':
        d['categories']='Categories not Found'
    if d['averageRating']=='No Description':
        d['averageRating']=0
    d['averageRating']*=30
    if d['averageRating'] >= 120:
        d['starcolor']='green'
    elif d['averageRating'] >= 90:
        d['starcolor']='blue'
    elif d['averageRating'] >= 60:
        d['starcolor']='yellow'
    elif d['averageRating'] >= 30:
        d['starcolor']='orange'
    else :
        d['starcolor']='red'
    return render(request, 'books/api_test.html', {'code':code , 'book':d , 'searchb':redirect_query ,'saleable':saleable , 'det':book ,'form':form})

#Add in cart form render

def get_add(request,code):
    user_tab=AddInCart.objects.filter(user=request.user)
    codes=[each.code for each in user_tab]
    if code in codes:
        return 0
    form = AddinCart(initial={'code': code , 'user':request.user})
    return form

#Remove from cart
def remove_cart(request):
    key = int(request.POST['pk'])
    tabl=AddInCart.objects.filter(id=key).delete()
    return redirect('books:cart')


#Add in cart render view and add

@login_required
def AddinCart_view(request):
    user = request.user
    table = AddInCart.objects.filter(user=user).order_by('-id')
    if request.method == "POST":
        form = AddinCart(request.POST)

        if form.is_valid():
            addincart_f = form.save(commit=False)
            addincart_f.user = request.user
            addincart_f.save()
    bookshelf=[]
    for item in table:
        d={}
        code=item.code
        querystring = str(str(code))
        googleapikey = "AIzaSyDragr-Pcph1OpaIGSvXlw-xwHsu3FLRXY"
        url_search = "https://www.googleapis.com/books/v1/volumes/" + str(querystring) +"?key=" + str(googleapikey) + "&country=IN"
        google_books = requests.get(url=url_search)
        books_json = google_books.json()
        book = books_json
        d={}
        for each in ['title', 'authors', 'description']:
            try:
                d[each] = book['volumeInfo'][each]
            except:
                d[each] = "No Description"
        try:
            d["imagelink"]= str(book["volumeInfo"]["imageLinks"]["thumbnail"])
        except:
            d['imagelink']= "https://safetyaustraliagroup.com.au/wp-content/uploads/2019/05/image-not-found.png"

        d['viewable'] = str(book['accessInfo']['embeddable'])

        d['id']=book['id']
        d['pk']=item.id

        d['authors']=str(d['authors'])[1:-1]
        lst_auth=d['authors'].split(',')
        fnl_lst_auth = []
        fnl_lst_auth.append(lst_auth[0][1:-1])
        for each in lst_auth[1:]:
            fnl_lst_auth.append(each[2:-1])
        d['authors']=", ".join(fnl_lst_auth)
        if d['authors'] == 'Descripti':
            d['authors']='Author Not Found'
        bookshelf.append(d)
    return render(request, "books/cart.html", {'table':table,'bookshelf':bookshelf})


