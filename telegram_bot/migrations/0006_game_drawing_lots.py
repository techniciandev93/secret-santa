# Generated by Django 3.2.23 on 2023-12-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0005_alter_gamer_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='drawing_lots',
            field=models.BooleanField(default=False, verbose_name='Жеребьёвка'),
        ),
    ]
