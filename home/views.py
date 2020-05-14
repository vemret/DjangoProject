from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from blog.models import Blog, Category, Images, Comment
from home.forms import SearchForm
from home.models import Setting, ContactFormMessage, ContactFormm


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Blog.objects.all()[:4]
    category = Category.objects.all()
    homeblogs = Blog.objects.all()[:4]
    lastblogs = Blog.objects.all().order_by('-id')[:4]
    randomblogs = Blog.objects.all().order_by('?')[:4]

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
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, }
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, }
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

    setting = Setting.objects.get(pk=1)
    form = ContactFormm()
    context = {'setting': setting, 'form': form}
    return render(request, 'iletisim.html', context)


def category_blogs(request,id,slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    blogs = Blog.objects.filter(category_id=id)
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
            blogs = Blog.objects.filter(title__icontains=query)
            context = {'blogs': blogs,
                       'category': category,
                       }
            return render(request, 'blogs_search.html', context)

        return HttpResponseRedirect('/')