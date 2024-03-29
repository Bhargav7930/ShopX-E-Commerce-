# Generated by Django 4.0.5 on 2022-07-05 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0005_order_shipping_address_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping_address',
            name='email',
            field=models.EmailField(default=True, max_length=255),
        ),
        migrations.AddField(
            model_name='shipping_address',
            name='phone',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AddField(
            model_name='shipping_address',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
