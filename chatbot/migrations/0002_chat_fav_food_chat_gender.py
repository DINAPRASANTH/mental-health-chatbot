# Generated by Django 5.0.3 on 2024-04-25 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='fav_food',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='chat',
            name='gender',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
