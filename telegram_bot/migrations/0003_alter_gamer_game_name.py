# Generated by Django 3.2.23 on 2023-12-15 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0002_auto_20231215_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamer',
            name='game_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='telegram_bot.game', verbose_name='Название игры'),
        ),
    ]
