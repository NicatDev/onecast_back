# Generated by Django 4.2 on 2023-05-15 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_alter_actorcategory_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='about_me',
            options={'verbose_name': 'about me', 'verbose_name_plural': 'about_me'},
        ),
    ]
