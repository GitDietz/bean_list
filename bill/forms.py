from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.utils.safestring import mark_safe
from .models import Customer, Job, Invoice, Resource, BillingRate, TimeItem


class CustomerForm(forms.ModelForm):
    """
    For gets driven from the list and will use the list reference
    """
    class Meta:
        model = Customer
        fields = ['name', 'business', 'contact', 'email', 'reference', 'active']
