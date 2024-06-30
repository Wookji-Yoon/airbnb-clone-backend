# Generated by Django 4.2.13 on 2024-06-30 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0003_alter_experience_category_alter_experience_owner_and_more'),
        ('rooms', '0006_alter_room_price_alter_room_rooms_alter_room_toilets'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0002_alter_review_experiences_alter_review_rooms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='experiences',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='experiences.experience'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rooms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='rooms.room'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]