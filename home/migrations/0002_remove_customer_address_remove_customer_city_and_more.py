# Generated by Django 4.0.5 on 2022-07-03 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='state',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='customer',
            name='auth_token',
            field=models.CharField(default=0, max_length=1200),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
