# Generated by Django 5.0 on 2023-12-31 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0016_genre_movie_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='quality',
            field=models.CharField(choices=[('hd', 'HD'), ('sd', 'SD')], default='hd', max_length=255),
        ),
    ]