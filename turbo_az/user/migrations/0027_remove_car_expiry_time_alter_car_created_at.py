# Generated by Django 5.0.4 on 2024-08-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0026_car_expiry_time_alter_car_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='expiry_time',
        ),
        migrations.AlterField(
            model_name='car',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Yaradılma vaxtı'),
        ),
    ]
