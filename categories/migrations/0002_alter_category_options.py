# Generated by Django 4.2.13 on 2024-06-15 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '카테고리들'},
        ),
    ]
