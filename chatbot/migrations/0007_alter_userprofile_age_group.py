# Generated by Django 5.0.3 on 2024-05-07 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0006_userprofile_age_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age_group',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
