# Generated by Django 3.2 on 2022-03-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220312_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='user',
        ),
        migrations.AddField(
            model_name='investment',
            name='investment',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='investor',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
