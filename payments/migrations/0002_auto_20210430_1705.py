# Generated by Django 3.1.7 on 2021-04-30 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberaccount',
            old_name='user_id',
            new_name='user',
        ),
    ]
