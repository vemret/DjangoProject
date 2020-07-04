import json

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from blog.models import Blog, Category, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormMessage, ContactFormm, UserProfile, FAQ


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Blog.objects.filter( status='True')[:5]
    category = Category.objects.all()
    homeblogs = Blog.objects.filter( status='True')[:5]
    lastblogs = Blog.objects.filter( status='True').order_by('-id')[:6]
    randomblogs = Blog.objects.filter( status='True').order_by('?')[:8]


    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'homeblogs': homeblogs,
               'lastblogs': lastblogs,
               'randomblogs': randomblogs
               }
    return render(request, 'index.html', context)




def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               }
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,
               'category': category,
               }
    return render(request, 'referanslar.html', context)


def iletisim(request):

    if request.method == 'POST': #Form Post eddildi ise
        form = ContactFormm(request.POST)
        if form.is_valid():
            data = ContactFormMessage() #model ile baglantı kur
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() # veri tabanı kayıt
            messages.success(request, "Mesajınız başarı ile gönderildi")
            return HttpResponseRedirect('/iletisim')

    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactFormm()
    context = {'setting': setting,
               'form': form,
               'category': category,
               }
    return render(request, 'iletisim.html', context)


def category_blogs(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    blogs = Blog.objects.filter(category_id=id, status='True')
    context = {'blogs': blogs,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'blogs.html', context)


def blog_detail(request, id, slug):
    category = Category.objects.all()  #suan kullanılmıyo sidebar cagırıcaksam
    blog = Blog.objects.get(pk=id)
    images = Images.objects.filter(blog_id=id)
    comments = Comment.objects.filter(blog_id=id, status='True')
    context = {'blog': blog,
               'category': category,
               'images': images,
               'comments': comments,
               }
    return render(request, 'blog_detail.html', context)

def blog_search(request):
    if request.method == 'POST':  # form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()  # access user session info.


            query = form.cleaned_data['query'] # formdan bilgiyi al
            catid = form.cleaned_data['catid']  # formdan bilgiyi al

            if catid == 0:
                blogs = Blog.objects.filter(title__icontains=query, status='True')
            else:
                blogs = Blog.objects.filter(title__icontains=query,category_id=catid, status='True')

            context = {'blogs': blogs,
                       'category': category,
                       }
            return render(request, 'blogs_search.html', context)

    return HttpResponseRedirect('/')

def blog_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        places = Blog.objects.filter(title__icontains=q)
        results = []
        for pl in places:
            place_json = {}
            place_json = pl.title
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "Opss! Giriş hatalı kullanıcı adınızı ve ya şifrenizi kontrol edin! :(")
            return HttpResponseRedirect('/login')


    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Hoş Geldiniz.. Sitemize başarılı bir şekilde üye oldunuz :)")
            return HttpResponseRedirect("/")


    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'signup.html', context)


def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status=True).order_by('ordernum')
    context = {
        'category': category,
        'faq': faq,
    }
    return render(request, 'faq.html', context)