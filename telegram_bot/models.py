import uuid

from django.contrib.auth.models import User
from django.db import models


class PriceRange(models.Model):
    min_price = models.DecimalField(verbose_name='Минимальная цена', max_digits=10, decimal_places=2)
    max_price = models.DecimalField(verbose_name='Максимальная цена', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Диапазон цены'
        verbose_name_plural = 'Диапазон цен'

    def __str__(self):
        return f'{self.min_price} - {self.max_price}'


class Game(models.Model):
    uuid = models.UUIDField(verbose_name='Идентификатор игры', default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name='Название игры', max_length=100)
    limit_cost = models.BooleanField(verbose_name='Ограничение стоимости подарка', null=True)
    price_ranges = models.ManyToManyField(PriceRange, verbose_name='Диапазон цены')
    start_registration_period = models.DateTimeField(verbose_name='Начало регистрации')
    end_registration_period = models.DateTimeField(verbose_name='Конец регистрации')
    shipping_date = models.DateField(verbose_name='Дата доставки подарка')
    drawing_lots = models.BooleanField(verbose_name='Жеребьёвка', default=False)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.name


class Gamer(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='ID игрока в телеграм')
    creator = models.ForeignKey(User, verbose_name='Создатель игры', on_delete=models.CASCADE, null=True, blank=True)
    game_name = models.ForeignKey(Game, verbose_name='Название игры', related_name='gamers',
                                  on_delete=models.CASCADE, blank=True, null=True)
    gamer = models.CharField(verbose_name='Имя игрока', max_length=100, blank=True)
    email = models.EmailField(verbose_name='Электронная почта', max_length=254, blank=True)
    vishlist = models.CharField(verbose_name='Список пожеланий', max_length=200, blank=True)
    santa_letter = models.TextField(verbose_name='Письмо Санте', blank=True, default='')

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'

    def __str__(self):
        return str(self.telegram_id)


class Sortition(models.Model):
    game = models.ForeignKey(Game, verbose_name='Игра', on_delete=models.CASCADE, related_name='sortitions')
    gifter = models.ForeignKey(Gamer, verbose_name='Даритель', on_delete=models.CASCADE, related_name='gifters')
    recipient = models.ForeignKey(Gamer, verbose_name='Получатель', on_delete=models.CASCADE, related_name='recipients')

    class Meta:
        verbose_name = 'Жеребьевка'
        verbose_name_plural = 'Жеребьевки'

    def __str__(self):
        return str(self.game.name)
