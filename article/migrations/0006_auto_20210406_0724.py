# Generated by Django 3.1.7 on 2021-04-06 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20210331_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Category')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='article.category', verbose_name='Category'),
        ),
    ]
