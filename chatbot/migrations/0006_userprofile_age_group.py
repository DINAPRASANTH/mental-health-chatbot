# Generated by Django 5.0.3 on 2024-05-01 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0005_remove_userprofile_fav_food_userprofile_lang_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age_group',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]