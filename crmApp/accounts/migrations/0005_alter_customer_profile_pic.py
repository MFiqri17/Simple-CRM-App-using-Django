# Generated by Django 4.0.1 on 2022-01-17 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customer_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='static/images'),
        ),
    ]