# Generated by Django 2.2.7 on 2020-09-19 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_forum_ask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='ask',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True),
        ),
    ]
