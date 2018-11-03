from django.contrib import admin
from django.utils.html import mark_safe

from .models import Post, Tag, Image
from .forms import PostForm, ImageForm


admin.site.site_header = "Blog administration"

# register with generic ModelAdmin
admin.site.register(Tag)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    readonly_fields = ('preview',)
    fieldsets = (
        (None, {'fields': ('name', 'title', 'tags', 'images', 'markdown')}),
        ('Preview', {'fields': ('preview',)}),
    )

    def preview(self, post):
        return mark_safe(
            '<div class="post" id="post_preview">'
            '<h1>' + post.title + '</h1>' + post.html() + '</div>')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageForm
