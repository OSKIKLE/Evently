from django.db import models
from django.contrib.auth.models import User

class Wydarzenie(models.Model):
    nazwa = models.CharField(max_length=200)
    miejsce = models.CharField(max_length=200)
    data = models.DateField()
    organizator = models.CharField(max_length=200)
    opis = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.nazwa

class Zapis(models.Model):
    wydarzenie = models.ForeignKey(Wydarzenie, on_delete=models.CASCADE, related_name='zapisy')
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    data_zapisu = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wydarzenie', 'uzytkownik') 