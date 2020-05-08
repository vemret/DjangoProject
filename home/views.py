from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from blog.models import Blog
from home.models import Setting, ContactFormMessage, ContactFormm


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Blog.objects.all()[:4]
    context = {'setting': setting, 'page': 'home', 'sliderdata':sliderdata}
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