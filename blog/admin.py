from django.contrib import admin

# Register your models here.
from blog.models import Category, Blog


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status']
    list_filter = ['status', 'category']

admin.site.register(Category,CategoryAdmin)
admin.site.register(Blog,BlogAdmin)