# Generated by Django 4.0.5 on 2022-06-16 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_alter_user_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
