from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from blog.models import CommentForm, Comment


def index(request):
    return HttpResponse("Blog Page!")

@login_required(login_url='/login') #check login
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST': #form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user #access user session info.

            data = Comment() #model ile baglantı kur
            data.user_id = current_user.id
            data.blog_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.ip = request.META.get('REMOTE_ADDR') #Client computer ip adres
            data.save() # veri tabanı kayıt

            messages.success(request, "Yorumunuz başarı ile gönderildi! :)")
            return HttpResponseRedirect(url)

        messages.warning(request, "Upppss bir sorun var! :(")
        return HttpResponseRedirect(url)