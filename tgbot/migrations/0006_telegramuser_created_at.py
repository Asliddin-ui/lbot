# Generated by Django 4.2.4 on 2023-09-04 14:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0005_alter_telegramuser_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]