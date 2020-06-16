from django.urls import path

from . import views

urlpatterns = [
    # ex: /home/
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('addblog/', views.addblog, name='addblog'),
    path('blog/', views.blog, name='blog'),
    path('blogedit/<int:id>', views.blogedit, name='blogedit'),
    path('blogdelete/<int:id>', views.blogdelete, name='blogdelete'),
    path('blogaddimage/<int:id>', views.blogaddimage, name='blogaddimage'),




    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),

]