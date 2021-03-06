import misaka
import mimetypes
import os
import re

from bs4 import BeautifulSoup

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from django.conf import settings


RE_FILENAME_IMG = re.compile(r'[a-z0-9\_]+\.(?:jpg|png|svg|gif)')
RE_MARKDOWN_IMG = re.compile(r'(?P<full>\!\[(?P<alt>.*)\]\((?P<filename>' + RE_FILENAME_IMG.pattern + r')\))')


class MarkdownRenderer:
    def __init__(self, post_model_obj=None):
        self.post = post_model_obj

    def escape_align_environment(self, text, reverse=False):
        if not reverse:
            text = re.sub(r'\\begin\{align\}', '$$BEGINALIGN', text)
            text = re.sub(r'\\end\{align\}', 'ENDALIGN$$', text)
        else:
            text = re.sub(r'\\\[BEGINALIGN', r'\\begin{align}', text)
            text = re.sub(r'ENDALIGN\\\]', r'\\end{align}', text)
        return text

    def escape(self, text, reverse=False):
        steps = [self.escape_align_environment]
        if reverse:
            steps = reversed(steps)
        for step in steps:
            text = step(text, reverse=reverse)
        return text

    def image_html(self, image_model_obj):
        filepath = os.path.join(settings.MEDIA_URL, image_model_obj.file.name)
        return (
            '<figure id="{filename}">'
            '<img class="post_image" src="{filepath}" alt="{filename}"/>'
            '<figcaption>'
            '<span class="figcaption_prefix">Figure: </span>{{caption}}'
            '</figcaption>'
            '</figure>'
            .format(
                filepath=filepath,
                filename=image_model_obj.filename))

    def render(self, markdown):
        if self.post is not None and self.post.id is not None:
            image_html = {img.filename: self.image_html(img) for img in self.post.images.all()}
            translate = {m['full']: image_html.get(m['filename'], "[ IMAGE NOT FOUND ]").format(caption=m['alt']) for m in RE_MARKDOWN_IMG.finditer(markdown)}
            for orig, repl in translate.items():
                markdown = markdown.replace(orig, repl)
        markdown = self.escape(markdown)
        html = misaka.html(markdown, extensions=['math', 'math-explicit', 'fenced-code', 'footnotes'], render_flags=[])
        html = self.escape(html, reverse=True)

        # open all links in a new window
        soup = BeautifulSoup(html, 'lxml')
        if soup.find('a') is not None:
            soup.find('a')['target'] = '_blank'
        html = str(soup)

        return html


@deconstructible
class FileValidator:
    """
    Validator for files, checking the size, extension and mimetype.

    Params
    ------
    restricted_basename: bool (default=True)
        Restrict basename to lowercase ascii, digits and underscores.
    allowed_extensions : sequence of str
        Allowed file extensions, e.g. ('txt', 'doc')
    allowed_mimetypes : sequence of str
        Allowed mimetypes, e.g. ('image/png', )
    min_size : int
        Minimum number of bytes allowed, e.g. 100
    max_size : int
        Maximum number of bytes allowed, e.g. 24*1024*1024 for 24 MiB

    Usage
    -----
    >>> from django.db import models
    >>>
    >>> MyModel(models.Model):
    ...     myfile = models.FileField(
    ...         validators=[FileValidator(max_size=24*1024*1024)],
    ...     )


    Note
    ----
    Adapted from github gist: https://gist.github.com/jrosebr1/2140738

    """
    RE_BASENAME = re.compile(r'[a-z0-9\_]+')

    # Error messages
    basename_message = _("Basename '%(basename)s' contains bad characters. Allowed characters are lowercase letters, digits and underscores.")
    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    min_size_message = _('The current file %(size)s, which is too small. The minumum file size is %(allowed_size)s.')
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, *args, **kwargs):
        self.restricted_basename = kwargs.pop('restricted_basename', True)
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.allowed_mimetypes = kwargs.pop('allowed_mimetypes', None)
        self.min_size = kwargs.pop('min_size', 0)
        self.max_size = kwargs.pop('max_size', None)

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """
        basename, ext = os.path.splitext(value.name)
        ext = ext[1:].lower()  # example: '.JPG' -> 'jpg'

        # Check the basename
        if self.restricted_basename and not self.RE_BASENAME.match(basename):
            message = self.basename_message % {'basename': basename}
            raise ValidationError(message)

        # Check the extension
        if self.allowed_extensions and ext not in self.allowed_extensions:
            message = self.extension_message % {
                'extension': ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }
            raise ValidationError(message)

        # Check the content type
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and mimetype not in self.allowed_mimetypes:
            message = self.mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }
            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }
            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_size)
            }
            raise ValidationError(message)
