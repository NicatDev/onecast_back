# Generated by Django 4.2 on 2023-05-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('castingapp', '0004_partners'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media/news'),
        ),
    ]
