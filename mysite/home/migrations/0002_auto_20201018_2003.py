# Generated by Django 3.0.2 on 2020-10-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='linkedin_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
