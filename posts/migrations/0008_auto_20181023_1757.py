# Generated by Django 2.1.2 on 2018-10-23 06:57

from django.db import migrations, models
import posts.models
import posts.utils


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20181022_1246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.FileField(unique=True, upload_to=posts.models.upload_to, validators=[posts.utils.FileValidator(allowed_extensions=('jpg', 'png', 'svg'), allowed_mimetypes=('image/jpg', 'image/png', 'image/svg', 'image/svg+xml'), restricted_basename=True)]),
        ),
    ]
