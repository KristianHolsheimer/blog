from django.contrib import admin
from django.utils.html import mark_safe

from .models import Post, Tag, Image
from .forms import PostForm, ImageForm


admin.site.site_header = "Blog administration"

# register with generic ModelAdmin
admin.site.register(Tag)


def put_live(modeladmin, request, queryset):
    for post in queryset:
        post.is_live = True
        post.save()


def take_down(modeladmin, request, queryset):
    for post in queryset:
        post.is_live = False
        post.save()


put_live.short_description = 'Put post live'
take_down.short_description = 'Take down post'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    readonly_fields = ('preview',)
    fieldsets = (
        (None, {'fields': ('is_live', 'name', 'title', 'category', 'tags', 'images', 'markdown')}),
        ('Preview', {'fields': ('preview',)}),
    )
    actions = [put_live, take_down]

    def preview(self, post):
        return mark_safe(
            '<div class="post" id="post_preview">'
            '<h1>' + post.title + '</h1>' + post.html() + '</div>')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageForm
