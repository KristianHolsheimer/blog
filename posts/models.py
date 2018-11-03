import os
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import mark_safe

from .utils import MarkdownRenderer, FileValidator, RE_FILENAME_IMG


# validators
tag_validator = RegexValidator(
    regex='^[a-z]+(?:-[a-z0-9]+)*$',
    message="Tag must consist of lowercase letters, digits and hyphens.",
    code='invalid_tag'
)
post_validator = RegexValidator(
    regex='^(?:new|edit|test|preview)*$',
    message="Name is reserved: 'new', 'edit' or 'test'.",
    code='invalid_name',
    inverse_match=True,
)
image_validator = FileValidator(
    restricted_basename=False,
    allowed_extensions=('jpg', 'png', 'svg'),
    allowed_mimetypes=('image/jpg', 'image/png', 'image/svg', 'image/svg+xml'),
)
image_filename_validator = RegexValidator(
    regex=RE_FILENAME_IMG,
    message="Please use a filename using lowercase letters, digits and underscores. Valid extensions are: 'jpg', 'png' or 'svg'",
    code='invalid_name',
    inverse_match=True,
)


def upload_to(model, filename):
    if isinstance(model, Image):
        prefix = "img/"
    else:
        raise NotImplementedError("upload_to is only implemented for Image models")
    ext = os.path.splitext(filename)[1].lower()  # e.g. 'photo.JPG' -> '.jpg'
    filepath = "{}{}{}".format(prefix, uuid.uuid4(), ext)
    return filepath


class Tag(models.Model):
    name = models.SlugField(
        max_length=30, unique=True, blank=False, null=False,
        validators=[tag_validator])

    def posts(self):
        return Post.objects.filter(tags__name__contains=self.name)

    def __str__(self):
        return self.name


class Image(models.Model):
    filename = models.CharField(
        max_length=30, unique=True, blank=False, null=False,
        validators=[post_validator])
    file = models.FileField(
        unique=True, blank=False, null=False, upload_to=upload_to,
        validators=[image_validator])

    def __str__(self):
        return self.filename


class Post(models.Model):
    name = models.SlugField(
        max_length=30, unique=True, blank=False, null=False,
        validators=[post_validator])
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    images = models.ManyToManyField(Image, blank=True)
    markdown = models.TextField()
    pub_date = models.DateField('date published', auto_now_add=True)

    def __str__(self):
        return self.title

    def html(self):
        md = MarkdownRenderer(self)
        html = md.render(self.markdown)
        return mark_safe(html)
