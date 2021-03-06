from django.db import models


# class Country(models.Model):
#     name = models.CharField(max_length=256)
#
#     def __unicode__(self):
#         return self.name


class Company(models.Model):
    code = models.CharField(blank=True, null=True, max_length=50)
    name = models.CharField(blank=True, null=True, max_length=256)
    country = models.CharField(blank=True, null=True, max_length=256)
    alpha = models.FloatField(blank=True, null=True, )
    beta = models.FloatField(blank=True, null=True, )

    def __unicode__(self):
        return self.name


class CompanyMonthly(models.Model):
    company = models.ForeignKey(Company,)
    month = models.DateField(blank=True, null=True, )
    std = models.FloatField(blank=True, null=True, )
    market_value = models.FloatField(blank=True, null=True, )
    book_value = models.FloatField(blank=True, null=True, )
    sales = models.FloatField(blank=True, null=True, )
    returns = models.FloatField(blank=True, null=True, )
    book_market_value = models.FloatField(blank=True, null=True, )

    def __unicode__(self):
        return str(self.company)


class MonthlyVP(models.Model):
    month = models.DateField()
    vp = models.FloatField(blank=True, null=True, )
    country = models.CharField(blank=True, null=True, max_length=256)

    def __unicode__(self):
        return str(self.month)


class DailyRF(models.Model):

    date = models.DateField(blank=True, null=True, )
    country = models.CharField(blank=True, null=True, max_length=256)
    rf = models.FloatField(blank=True, null=True, )
    rm_rf = models.FloatField(blank=True, null=True, )

    def __unicode__(self):
        return self.country + ' - '+ str(self.date)

class CompanyDaily(models.Model):
    company = models.ForeignKey(Company,)
    date = models.DateField(blank=True, null=True, )
    price = models.FloatField(blank=True, null=True, )
    returns = models.FloatField(blank=True, null=True,)
    real_returns = models.FloatField(blank=True, null=True,)

    def __unicode__(self):
        return self.company.name + ' - '+ str(self.date)

class MonthlySentiment(models.Model):
    month = models.DateField()
    sentiment = models.FloatField(blank=True, null=True, )
    country = models.CharField(blank=True, null=True, max_length=256)

    def __unicode__(self):
        return str(self.month)


class MonthlyGroups(models.Model):
    month = models.DateField()
    group_number = models.IntegerField()
    type = models.CharField(max_length=128)
    country = models.CharField(blank=True, null=True, max_length=256)
    average_returns = models.FloatField(blank=True, null=True, )
    lastmonth_sentiment = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return str(self.month)

class MonthlyGroupsResult(models.Model):
    group_number = models.IntegerField()
    type = models.CharField(max_length=128)
    result = models.FloatField(blank=True, null=True, )
    country = models.CharField(blank=True, null=True, max_length=256)

    def __unicode__(self):
        return str(self.group_number)
