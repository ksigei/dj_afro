# Generated by Django 5.0 on 2023-12-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_remove_comment_movie'),
        ('movies', '0010_remove_movie_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='comments',
            field=models.ManyToManyField(blank=True, to='comments.comment'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
