# Generated by Django 3.1.1 on 2021-07-14 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210714_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
