# Generated by Django 2.1.2 on 2018-11-22 11:41

from django.db import migrations, models
import posts.models
import posts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_post_is_live'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Data Science'), (1, 'Engineering')], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.FileField(unique=True, upload_to=posts.models.upload_to, validators=[posts.utils.FileValidator(allowed_extensions=('jpg', 'png', 'svg'), allowed_mimetypes=('image/jpeg', 'image/png', 'image/svg', 'image/svg+xml'), restricted_basename=False)]),
        ),
    ]
