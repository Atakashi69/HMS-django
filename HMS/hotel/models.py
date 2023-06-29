from django.conf import settings
from django.db import models

# Create your models here.
class Room(models.Model):
    number = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.number}. Вместимость = {self.capacity}, Цена за ночь = {self.price}'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f'{self.user} забронировал комнату {self.room.number} с {self.check_in} по {self.check_out}'

