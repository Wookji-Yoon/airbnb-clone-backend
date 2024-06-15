# Generated by Django 4.2.13 on 2024-06-15 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiences', '0002_experience_category_alter_perk_details_and_more'),
        ('rooms', '0004_room_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('room_check_in_date', models.DateField(blank=True, null=True)),
                ('room_check_out_date', models.DateField(blank=True, null=True)),
                ('experience_time', models.DateTimeField(blank=True, null=True)),
                ('guests', models.PositiveIntegerField()),
                ('experience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='experiences.experience')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rooms.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
