# Generated by Django 4.0.5 on 2022-07-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_shipping_address_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(default=True, upload_to='profile'),
        ),
    ]
