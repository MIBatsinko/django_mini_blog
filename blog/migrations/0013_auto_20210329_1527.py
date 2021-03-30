# Generated by Django 3.1.7 on 2021-03-29 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_userprofile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='ip',
            field=models.CharField(max_length=15, verbose_name='IP address'),
        ),
        migrations.AlterField(
            model_name='ratingstar',
            name='value',
            field=models.SmallIntegerField(default=0, verbose_name='Value'),
        ),
    ]