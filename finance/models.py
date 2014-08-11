from django.db import models


class CompanyMonthly(models.Model):
    company = models.CharField(blank=True, null=True, max_length=128)
    code = models.CharField(blank=True, null=True, max_length=50)
    month = models.DateField(blank=True, null=True, )
    std = models.FloatField(blank=True, null=True, )
    market_value = models.FloatField(blank=True, null=True, )
    book_value = models.FloatField(blank=True, null=True, )
    sales = models.FloatField(blank=True, null=True, )
    returns = models.FloatField(blank=True, null=True, )

    def __unicode__(self):
        return self.company

