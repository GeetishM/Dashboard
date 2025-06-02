from django.db import models

class BudgetData(models.Model):
    shop = models.TextField(primary_key=True)
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
        managed = False
        db_table = 'zedw_budget_dash_v'  # This model uses the first table

# Add a NEW model for the second table:
class BudgetDataOther(models.Model):
    shop = models.TextField(primary_key=True)
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
        managed = False
        db_table = 'zedw_budget_dash_other_v'  # This model uses the second table

# Remove or comment out pr_no if it does not exist in your DB view
class PrRelPendLive(models.Model):
    pur_grp_grp = models.CharField(max_length=100, primary_key=True)  # Set as primary key
    pr_date = models.DateField(null=True, blank=True)
    pur_grp = models.CharField(max_length=50, null=True, blank=True)
    plant = models.CharField(max_length=50, null=True, blank=True)
    line_item = models.CharField(max_length=20, null=True, blank=True)
    mat_code = models.CharField(max_length=50, null=True, blank=True)
    mat_desc = models.TextField(null=True, blank=True)
    rel_pend_with = models.CharField(max_length=100, null=True, blank=True)
    pur_officer = models.CharField(max_length=100, null=True, blank=True)
    ins_date = models.DateField(null=True, blank=True)
    pr_text = models.TextField(null=True, blank=True)
    pr_value = models.FloatField(null=True, blank=True)
    sug_mod_tend = models.CharField(max_length=100, null=True, blank=True)
    fund_center = models.CharField(max_length=100, null=True, blank=True)
    shop = models.CharField(max_length=100, null=True, blank=True)
    item_value = models.FloatField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    del_date = models.DateField(null=True, blank=True)
    ext_mat_grp = models.CharField(max_length=100, null=True, blank=True)
    chng_date = models.DateField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'pr_rel_pend_live'


class PrEnqStatusLive(models.Model):
    pur_grp_grp = models.CharField(max_length=100, primary_key=True)  # Set as primary key
    pr_date = models.DateField(null=True, blank=True)
    pur_grp = models.CharField(max_length=50, null=True, blank=True)
    plant = models.CharField(max_length=50, null=True, blank=True)
    line_item = models.CharField(max_length=20, null=True, blank=True)
    mat_code = models.CharField(max_length=50, null=True, blank=True)
    mat_desc = models.TextField(null=True, blank=True)
    mat_grp = models.CharField(max_length=50, null=True, blank=True)
    fnl_rel_date = models.DateField(null=True, blank=True)
    enq_no = models.CharField(max_length=50, null=True, blank=True)
    enq_date = models.DateField(null=True, blank=True)
    enq_pend_days = models.IntegerField(null=True, blank=True)
    po_pend_days = models.IntegerField(null=True, blank=True)
    enq_mode = models.CharField(max_length=50, null=True, blank=True)
    pur_officer = models.CharField(max_length=100, null=True, blank=True)
    ins_date = models.DateField(null=True, blank=True)
    cfn = models.CharField(max_length=50, null=True, blank=True)
    pr_text = models.TextField(null=True, blank=True)
    pr_value = models.FloatField(null=True, blank=True)
    sug_mod_tend = models.CharField(max_length=100, null=True, blank=True)
    fund_center = models.CharField(max_length=100, null=True, blank=True)
    shop = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'pr_enq_status_live'


class PendPoStatusLive(models.Model):
    pur_grp_grp = models.CharField(max_length=100, primary_key=True)  # Set as primary key
    line_item = models.CharField(max_length=20, null=True, blank=True)
    sche_line_item = models.CharField(max_length=20, null=True, blank=True)
    po_date = models.DateField(null=True, blank=True)
    pur_grp = models.CharField(max_length=50, null=True, blank=True)
    plant = models.CharField(max_length=50, null=True, blank=True)
    mat_code = models.CharField(max_length=50, null=True, blank=True)
    mat_desc = models.TextField(null=True, blank=True)
    mat_grp = models.CharField(max_length=50, null=True, blank=True)
    del_date = models.DateField(null=True, blank=True)
    sch_qty = models.FloatField(null=True, blank=True)
    rcvd_qty = models.FloatField(null=True, blank=True)
    bal_qty = models.FloatField(null=True, blank=True)
    uom = models.CharField(max_length=20, null=True, blank=True)
    item_value = models.FloatField(null=True, blank=True)
    vendor_code = models.CharField(max_length=50, null=True, blank=True)
    vendor_name = models.CharField(max_length=200, null=True, blank=True)
    ins_date = models.DateField(null=True, blank=True)
    tender_mode = models.CharField(max_length=100, null=True, blank=True)
    pur_officer = models.CharField(max_length=100, null=True, blank=True)
    vend_email = models.EmailField(max_length=200, null=True, blank=True)
    fund_center = models.CharField(max_length=100, null=True, blank=True)
    shop = models.CharField(max_length=100, null=True, blank=True)
    cfn_number = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'pend_po_status_live'
