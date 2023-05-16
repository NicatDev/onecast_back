# Generated by Django 4.1.2 on 2023-04-12 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_registermessage_delete_myuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermessage',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='registermessage',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='media/images'),
        ),
        migrations.AlterField(
            model_name='registermessage',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='media/images'),
        ),
        migrations.AlterField(
            model_name='registermessage',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='media/images'),
        ),
    ]
