# Generated by Django 2.1.2 on 2018-10-31 10:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20181024_1410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AddField(
            model_name='image',
            name='post_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='filename',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_name', inverse_match=True, message="Name is reserved: 'new', 'edit' or 'test'.", regex='^(?:new|edit|test|preview)*$')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='name',
            field=models.SlugField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_name', inverse_match=True, message="Name is reserved: 'new', 'edit' or 'test'.", regex='^(?:new|edit|test|preview)*$')]),
        ),
    ]
