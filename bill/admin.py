from django.contrib import admin

from .models import Customer, Job, Invoice, Resource, BillingRate, TimeItem


admin.site.register(Customer)
admin.site.register(Job)
admin.site.register(Invoice)
admin.site.register(Resource)
admin.site.register(BillingRate)
admin.site.register(TimeItem)

