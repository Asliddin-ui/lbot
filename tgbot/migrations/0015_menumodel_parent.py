# Generated by Django 4.2.4 on 2023-09-08 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0014_menumodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='menumodel',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='tgbot.menumodel'),
        ),
    ]
