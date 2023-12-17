from django.db import models


class Game(models.Model):
    name_of_game = models.CharField(
        verbose_name='Название игры',
        max_length=25
    )
    creators_id = models.PositiveBigIntegerField(
        verbose_name='ID создателя игры в телеграмме'
    )
    cost_of_the_gift = models.CharField(
        verbose_name='Стоимость подарка',
        max_length=25
    )
    start_of_registration = models.DateTimeField(
        verbose_name='Начало регистрации'
    )
    end_of_registration = models.DateTimeField(
        verbose_name='Конец регистрации'
    )
    departure_date = models.DateTimeField(
        verbose_name='Дата отправки подарка'
    )
    link_to_the_game = models.EmailField(
        verbose_name='Ссылка на игру'
    )

    def __str__(self):
        return f'{self.name_of_game} {self.start_of_registration} - {self.end_of_registration}'

    class Meta:
        verbose_name = 'Игру'
        verbose_name_plural = 'Игры'
        ordering = ['-start_of_registration']


class Patricipants(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='Игра'
    )
    id_user = models.PositiveBigIntegerField(
        verbose_name='ID игрока в телеграмме'
    )
    name = models.TextField(
        verbose_name='Имя игрока'
    )
    e_mail = models.EmailField(
        verbose_name='Электронная почта'
    )
    interests = models.TextField(
        verbose_name='Интересы/увлечения',
        max_length=75
    )
    letter_to_santa = models.TextField(
        verbose_name='Письмо Санте',
        max_length=200
    )

    def __str__(self):
        return f'{self.game} {self.name}'

    class Meta:
        verbose_name = 'Участника'
        verbose_name_plural = 'Участники'
        ordering = ['id']


class Givers(models.Model):
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        verbose_name='Игра'
    )
    givers = models.OneToOneField(
        Patricipants,
        on_delete=models.CASCADE,
        verbose_name='Кто дарит'
    )
    recipient = models.TextField(
        verbose_name='Кому дарит'
    )

    def __str__(self):
        return f'{self.game} {self.givers} - {self.recipient}'

    class Meta:
        verbose_name = 'Дарители'
        verbose_name_plural = 'Дарители'
