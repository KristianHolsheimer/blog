from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Tag
from .forms import PostForm


def index(request):
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


def edit(request, post_name=None):
    try:
        post = Post.objects.get(name=post_name)
        form = PostForm(instance=post)
    except Post.DoesNotExist:
        post = None
        form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        # print('form:', form)
        if form.is_valid():
            if 'preview' in request.POST:
                print('preview:', request.POST)
                post = form.save(commit=False)
                print(form['tags'])
            elif 'save' in request.POST:
                print('save:', request.POST)
                post = form.save()
                # TODO: implement 'add image' functionality
                return redirect('/posts/{}'.format(post.name), permanent=True)
            else:
                raise NotImplementedError("So far, only implemented 'Preview' and 'Save' buttons")

    return render(request, 'posts/edit.html', {'form': form, 'post': post})
