from django.shortcuts import render, get_object_or_404

from .models import Post, Tag


def index(request):
    raise Exception("test message")
    posts = Post.objects.order_by('-pub_date')[:5]
    tags = Tag.objects.order_by('name')
    context = {'posts': posts, 'tags': tags}
    return render(request, 'posts/index.html', context)


def post(request, post_name):
    post_obj = get_object_or_404(Post, name=post_name)
    return render(request, 'posts/post_site.html', {'post': post_obj})


def tag(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)
    return render(request, 'posts/tag.html', {'tag': tag_obj})
