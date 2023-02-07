from django.contrib import admin

from .models import List


# class ListModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'purpose', 'manager', 'members', 'leaders', 'disabled']
#
#     class Meta:
#         model = List


admin.site.register(List)  # , ListModelAdmin
