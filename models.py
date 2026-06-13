from django.db import models


class SubAllotmentAdvice(models.Model):
    REGION_CHOICES = [
        ('1', 'Region 1'), ('2', 'Region 2'), ('3', 'Region 3'),
        ('4A', 'Region 4A'), ('4B', 'Region 4B'), ('5', 'Region 5'),
        ('6', 'Region 6'), ('7', 'Region 7'), ('8', 'Region 8'),
        ('9', 'Region 9'), ('10', 'Region 10'), ('11', 'Region 11'),
        ('12', 'Region 12'), ('13', 'Region 13 - Caraga'),
        ('CAR', 'CAR'), ('NCR', 'NCR'), ('BARMM', 'BARMM'),
    ]   

    advice_number = models.CharField(max_length=100)
    date                 = models.DateField(blank=True, null=True)
    calendar_year        = models.IntegerField(default=2025)
    region               = models.CharField(max_length=10, choices=REGION_CHOICES, default='13')
    to_office            = models.CharField(max_length=200, default='REGIONAL IRRIGATION MANAGER', blank=True)
    to_location          = models.CharField(max_length=200, blank=True)
    fund_code            = models.CharField(max_length=20, blank=True, default='501')
    gaa_saro_number      = models.CharField(max_length=200, blank=True)
    object_code          = models.CharField(max_length=50, blank=True, default='')
    description          = models.CharField(max_length=500, blank=True, default='')
    total_amount         = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    amount_in_words      = models.CharField(max_length=500, blank=True)
    certified_by_name    = models.CharField(max_length=200, blank=True)
    certified_by_title   = models.CharField(max_length=200, blank=True)
    recommended_by_name  = models.CharField(max_length=200, blank=True)
    recommended_by_title = models.CharField(max_length=200, blank=True)
    approved_by_name     = models.CharField(max_length=200, blank=True)
    approved_by_title    = models.CharField(max_length=200, blank=True)
    ada_number           = models.CharField(max_length=100, blank=True, null=True)
    ada_date             = models.DateField(blank=True, null=True)
    ada_amount           = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sub-Allotment Advice'
        verbose_name_plural = 'Sub-Allotment Advices'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.advice_number}"


class ProvinceAllotment(models.Model):
    sub_allotment  = models.ForeignKey(SubAllotmentAdvice, on_delete=models.CASCADE, related_name='province_allotments')
    province_name  = models.CharField(max_length=200)
    province_total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    order          = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.province_name} — ₱{self.province_total}"


class CISAllotment(models.Model):
    province_allotment = models.ForeignKey(ProvinceAllotment, on_delete=models.CASCADE, related_name='cis_allotments')
    cis_name = models.CharField(max_length=200)
    amount   = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.cis_name} — ₱{self.amount}"


class AllotmentStatement(models.Model):
    
    project_name       = models.CharField(max_length=500)
    ada_number         = models.CharField(max_length=100)
    allotment_received = models.DecimalField(max_digits=15, decimal_places=2)
    ada_received       = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    object_code        = models.CharField(max_length=100, blank=True)
    date               = models.DateField()
    remarks            = models.TextField(blank=True)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Allotment Statement'
        verbose_name_plural = 'Allotment Statements'
        ordering = ['-date']

    def __str__(self):
        return f"{self.ada_number} — {self.project_name}"


# ── Dropdown Master Tables ────────────────────────────────────────

class GAASAROMaster(models.Model):
    """Master list of GAA/SARO Numbers."""
    value = models.CharField(max_length=300, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'GAA/SARO Master'
        verbose_name_plural = 'GAA/SARO Masters'
        ordering = ['value']

    def __str__(self):
        return self.value


class ObjectCodeMaster(models.Model):
    """Master list of Object Codes."""
    value = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Object Code Master'
        verbose_name_plural = 'Object Code Masters'
        ordering = ['value']

    def __str__(self):
        return self.value


class DescriptionMaster(models.Model):
    """Master list of Project Descriptions."""
    value = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Description Master'
        verbose_name_plural = 'Description Masters'
        ordering = ['value']

    def __str__(self):
        return self.value


class AdviceNumberMaster(models.Model):
    """Master list of Advice of Sub-Allotment Numbers."""
    value = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Advice Number Master'
        verbose_name_plural = 'Advice Number Masters'
        ordering = ['-created_at']

    def __str__(self):
        return self.value


class CISMaster(models.Model):
    """Master list of CIS Names per Province."""
    province = models.CharField(max_length=200)
    cis_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'CIS Master'
        verbose_name_plural = 'CIS Masters'
        ordering = ['province', 'cis_name']
        unique_together = ['province', 'cis_name']

    def __str__(self):
        return f"{self.province} — {self.cis_name}"


class ProgramOfWork(models.Model):
    OFFICE_CHOICES = [
        ('ADN', 'Agusan del Norte'),
        ('ADS', 'Agusan del Sur'),
        ('SDN', 'Surigao del Norte'),
        ('SDS', 'Surigao del Sur'),
        ('RIO', 'Regional Irrigation Office'),
    ]

    advice    = models.ForeignKey(SubAllotmentAdvice, on_delete=models.CASCADE, related_name='programs_of_work')
    office    = models.CharField(max_length=10, choices=OFFICE_CHOICES)
    province  = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Program of Work'
        verbose_name_plural = 'Programs of Work'
        ordering = ['-created_at']
        unique_together = ['advice', 'office', 'province']

    def __str__(self):
        return f"{self.advice.advice_number} — {self.office} — {self.province}"


class ProgramOfWorkItem(models.Model):
    program     = models.ForeignKey(ProgramOfWork, on_delete=models.CASCADE, related_name='items')
    item        = models.CharField(max_length=100)
    pow_amount  = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    imo_amount  = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    mo_amount   = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['program', 'item']

    def __str__(self):
        return f"{self.program} — {self.item}"
