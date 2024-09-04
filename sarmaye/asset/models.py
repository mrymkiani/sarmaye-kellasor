from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=100)
    january = models.IntegerField()
    february = models.IntegerField()
    march = models.IntegerField()
    april = models.IntegerField()
    may = models.IntegerField()
    june = models.IntegerField()
    july = models.IntegerField()
    august = models.IntegerField()
    september = models.IntegerField()
    october = models.IntegerField()
    november = models.IntegerField()
    december = models.IntegerField()

    def __str__(self) -> str:
        return self.name
