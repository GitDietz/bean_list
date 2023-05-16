from datetime import date
from django.db import models
from django.db.models.functions import Lower
from django.conf import settings
from django.urls import reverse


# ## Model Managers ## #
class CustomerManager(models.Manager):
    def all(self):
        qs = super(CustomerManager, self).all()
        return qs

    def active(self):
        qs = super(CustomerManager, self).filter(active=True)
        return qs

    def inactive(self):
        qs = super(CustomerManager, self).filter(active=False)
        return qs


# ## Models ## #

class Customer(models.Model):
    """
    The main object - all jobs and billing will roll up to customer
    Mod 10/22
    """
    name = models.CharField(max_length=100, unique=True)
    business = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    contact = models.CharField(max_length=100, unique=False)
    email = models.EmailField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    objects = CustomerManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class Job(models.Model):
    """
    The object - will collect time expenditure and invoices
    Mod 10/22
    """
    name = models.CharField(max_length=100, unique=True)
    purpose = models.CharField(max_length=200, blank=False)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    # objects = CustomerManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class Invoice(models.Model):
    """
    The object - will collect time expenditure and invoices
    Mod 10/22
    """
    name = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created = models.DateField(auto_now=False, auto_now_add=True)
    issued = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    total_exc = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total_gst = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total_inc = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    # objects = CustomerManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class Resource(models.Model):
    """
    The object - person or equipment
    Mod 10/22
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=False, null=False)
    is_person = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()


class BillingRate(models.Model):
    """
    The object - person or equipment
    Mod 10/22
    """
    BILL_CHOICE = [('h', 'Hour'), ('d', 'Day')]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    rate = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    billing_per = models.CharField(max_length=2, choices=BILL_CHOICE, default='h', blank=False, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.resource.name + ' on ' + self.job.name.title()


class TimeItem(models.Model):
    """
    The object - will collect time expenditure and invoices
    Mod 10/22
    """
    activity = models.CharField(max_length=100, unique=True)
    date_of = models.DateField(default=date.today)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    started = models.DateTimeField()
    ended = models.DateTimeField()
    hrs = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    bill_at = models.CharField(max_length=2, default='h', blank=False, null=False)
    bill = models.BooleanField(null=False, blank=False, default=True)
    total_exc = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total_gst = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    total_inc = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)

    # objects = CustomerManager()

    def __str__(self):
        return self.activity.title() + str(self.id)
