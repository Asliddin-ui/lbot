# Generated by Django 4.2.4 on 2023-09-08 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0011_alter_telegramuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='cat',
            field=models.ManyToManyField(to='tgbot.categorymodel'),
        ),
    ]