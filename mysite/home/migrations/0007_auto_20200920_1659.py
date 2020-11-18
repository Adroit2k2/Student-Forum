# Generated by Django 2.2.7 on 2020-09-20 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200919_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiler', to=settings.AUTH_USER_MODEL),
        ),
    ]