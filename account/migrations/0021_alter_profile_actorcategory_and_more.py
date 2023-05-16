# Generated by Django 4.2 on 2023-05-16 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_about_me_language_alter_about_me_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='actorCategory',
            field=models.ManyToManyField(blank=True, related_name='actortalents', to='account.actorcategory'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='modelCategory',
            field=models.ManyToManyField(blank=True, related_name='modeltalents', to='account.modelcategory'),
        ),
    ]
