# Generated by Django 5.1.3 on 2024-11-22 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='movie',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='movies',
            field=models.ManyToManyField(to='app.movie'),
        ),
    ]
