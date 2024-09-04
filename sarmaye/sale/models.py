from django.db import models
from django.contrib.auth.models import User
from asset.models import Asset

class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset =  models.ForeignKey(Asset, on_delete=models.CASCADE)
    start_month = models.CharField(max_length=100)
    end_month = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    given_money = models.IntegerField()
    profit = models.FloatField()
    percentage = models.FloatField()

    def __str__(self) -> str:
        return f"{self.asset}, {self.start_month} to {self.end_month}, profit = {self.profit}, percentage = {self.percentage}"