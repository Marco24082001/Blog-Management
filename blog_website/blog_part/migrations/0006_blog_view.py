# Generated by Django 4.0.5 on 2022-06-16 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_part', '0005_alter_blog_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='view',
            field=models.IntegerField(default=0),
        ),
    ]