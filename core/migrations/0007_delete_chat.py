# Generated by Django 4.1.7 on 2023-05-12 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_rename_chats_chat'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Chat',
        ),
    ]