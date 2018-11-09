import logging
from django.shortcuts import render, get_object_or_404

from .models import Post, Tag

logger = logging.getLogger(__name__)


def log_request(view):
    def view_that_also_logs(request, *args, **kwargs):
        logger.debug('request.__dict__', extra={'request': request.__dict__})
        return view(request, *args, **kwargs)
    return view_that_also_logs


@log_request
def index(request):
    posts = Post.objects.filter(is_live=True).order_by('-pub_date')[:5]
    tags = Tag.objects.order_by('name')
    context = {'posts': posts, 'tags': tags}
    return render(request, 'posts/index.html', context)


@log_request
def post(request, post_name):
    logger.debug(dict(request))
    post_obj = get_object_or_404(Post, name=post_name, is_live=True)
    return render(request, 'posts/post_site.html', {'post': post_obj})


@log_request
def tag(request, tag_name):
    logger.debug(dict(request))
    tag_obj = get_object_or_404(Tag, name=tag_name)
    return render(request, 'posts/tag_site.html', {'tag': tag_obj})
