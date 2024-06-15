# Generated by Django 4.2.13 on 2024-06-15 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='kind',
            field=models.CharField(choices=[('room', 'Room'), ('experience', 'Experience')], default='room', max_length=30),
            preserve_default=False,
        ),
    ]
