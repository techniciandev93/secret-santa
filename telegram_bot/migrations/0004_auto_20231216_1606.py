# Generated by Django 3.2.23 on 2023-12-16 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0003_alter_gamer_game_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='end_registration_period',
            field=models.DateTimeField(verbose_name='Конец регистрации'),
        ),
        migrations.AlterField(
            model_name='game',
            name='start_registration_period',
            field=models.DateTimeField(verbose_name='Начало регистрации'),
        ),
    ]