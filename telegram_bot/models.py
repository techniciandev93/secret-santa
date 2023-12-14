from django.db import models


class Game(models.Model):
    name = models.CharField('Название игры', max_length=100, unique=True)
    limit_cost = models.BooleanField("Ограничение стоимости подарка", null=True, db_index=True)
    LIMITS_CHOISES = [
        ('no limits', 'нет ограничения'),
        ('< 500', 'до 500 рублей'),
        ('500-1000', '500-1000 рублей'),
        ('1000-2000', '1000-2000 рублей')
    ]
    limits = models.CharField('Стоимость подарка', max_length=20, choices=LIMITS_CHOISES, default='no limits')
    REGISTRATION_CHOISES = [
        ('25.12.2023', 'до 25.12.2023'),
        ('31.12.2023', 'до 31.12.2023')
    ]
    registration_period = models.CharField('Период регистрации', max_length=20, choices=REGISTRATION_CHOISES, default='31.12.2023')
    shipping_date = models.DateField('Дата доставки подарка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"


class Gamer(models.Model):
    game_name = models.ForeignKey(Game, verbose_name="Название игры", on_delete=models.CASCADE)
    gamer = models.CharField('Имя игрока', max_length=100)
    email = models.EmailField('Электронная почта', max_length=254)
    vishlist = models.CharField('Список пожеланий', max_length=200)
    santa_letter = models.TextField('Письмо Санте', blank=True, null=True)

    def __str__(self):
        return self.gamer

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"


class Sortition(models.Model):
    game_name = models.ForeignKey(Game, verbose_name='Название игры', on_delete=models.CASCADE)
    gifter = models.ForeignKey(Gamer, verbose_name='Даритель', on_delete=models.CASCADE, related_name='gifter')
    recipient = models.ForeignKey(Gamer, verbose_name='Получатель', on_delete=models.CASCADE, related_name='recipient')

    def __str__(self):
        return str(self.game_name)

    class Meta:
        verbose_name = "Жеребьевка"
        verbose_name_plural = "Жеребьевки"



