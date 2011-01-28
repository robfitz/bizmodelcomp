from django.shortcuts import render_to_response, get_object_or_404
from blog.models import *



def latest(request):

    posts = BlogPost.objects.filter(is_draft=False)[:5]
    categories = Category.objects.all()

    return render_to_response('blog/latest.html', locals())



def post(request, post_url):

    post = get_object_or_404(BlogPost, url=post_url)

    return render_to_response('blog/post.html', locals())
    
    
def category(request, name):
        
    categories = get_object_or_404(Category, name=name)
    posts = BlogPost.objects.filter(categories=categories)[:5]
    
    return render_to_response('blog/category.html', locals())