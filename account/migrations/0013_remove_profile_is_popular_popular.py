# Generated by Django 4.2 on 2023-05-10 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_remove_profile_category_profile_actorcategory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_popular',
        ),
        migrations.CreateModel(
            name='Popular',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_photo', models.ImageField(upload_to='media/covers')),
                ('is_active', models.BooleanField(default=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
    ]
