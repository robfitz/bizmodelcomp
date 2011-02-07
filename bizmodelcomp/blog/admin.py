from django.contrib import admin
from bizmodelcomp.blog.models import *
 
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('custom_title', 'url', 'created',)
    list_filter = ('categories',)
    filter_horizontal = ('categories',)

admin.site.register(Category)
admin.site.register(BlogPost, BlogPostAdmin)