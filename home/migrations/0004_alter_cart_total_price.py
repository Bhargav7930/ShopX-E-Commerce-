# Generated by Django 4.0.5 on 2022-07-04 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_cart_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
