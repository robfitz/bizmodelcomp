from django.shortcuts import render_to_response, get_object_or_404
from blog.models import *



def latest(request):

    posts = BlogPost.objects.filter(is_draft=False)[:10]

    return render_to_response('blog/latest.html', locals())



def post(request, post_url):

    post = get_object_or_404(BlogPost, url=post_url)

    return render_to_response('blog/post.html', locals())
