# Generated by Django 4.2.4 on 2023-09-04 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(blank=True, default=None, max_length=255)),
                ('name_ru', models.CharField(blank=True, default=None, max_length=255)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RegionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(blank=True, default=None, max_length=255)),
                ('name_ru', models.CharField(blank=True, default=None, max_length=255)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_uz', models.CharField(blank=True, default=None, max_length=255)),
                ('name_ru', models.CharField(blank=True, default=None, max_length=255)),
                ('name_en', models.CharField(blank=True, default=None, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('telegram_user_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('language', models.CharField(default='uz', max_length=2)),
                ('rating_count', models.IntegerField(default=0)),
                ('rating_stars', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tgbot.categorymodel')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tgbot.regionmodel')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tgbot.rolemodel')),
            ],
        ),
    ]
