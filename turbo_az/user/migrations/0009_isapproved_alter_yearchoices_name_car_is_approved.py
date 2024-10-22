# Generated by Django 5.0.6 on 2024-07-31 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_yearchoices_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsApproved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Status')),
            ],
        ),
        migrations.AlterField(
            model_name='yearchoices',
            name='name',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='car',
            name='is_approved',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.isapproved', verbose_name='Status'),
        ),
    ]
