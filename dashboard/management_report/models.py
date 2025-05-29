from django.db import models

class BudgetData(models.Model):
    shop = models.TextField(primary_key=True)  # Set as primary key
    fonds = models.TextField()
    fictr = models.TextField()
    citem = models.TextField()
    farea = models.TextField()
    fwaer = models.TextField()
    gjahr = models.IntegerField()
    fikrs = models.TextField()
    sbudget = models.FloatField()
    budget = models.FloatField()
    payment = models.IntegerField()
    bud_pmt = models.FloatField()
    invoice = models.FloatField()
    bud_inv = models.FloatField()
    opitems = models.FloatField()
    av_budget = models.FloatField()
    fund_center = models.TextField()

    class Meta:
        managed = False  # Don't create/migrate this table
        db_table = 'zedw_budget_dash_v'

