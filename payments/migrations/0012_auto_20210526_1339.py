# Generated by Django 3.1.7 on 2021-05-26 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_auto_20210526_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberaccount',
            name='card_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]