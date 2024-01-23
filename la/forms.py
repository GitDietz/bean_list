from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from django.utils.safestring import mark_safe
from .models import Item, Merchant, List, MasterList, MasterCategories, MasterItem


class NewListCreateForm(forms.ModelForm):
    """
    for existing members that want to create a new list
    """
    joining = forms.CharField(label='List to create', max_length=100)
    purpose = forms.CharField(label='What is this list for?', max_length=200)

    class Meta:
        model = List
        fields = ['joining', 'purpose']

    def clean(self):
        cleaned_data = super().clean()
        join = cleaned_data.get('joining', None)
        purp = cleaned_data.get('purpose', None)
        return cleaned_data

    def clean_joining(self):
        target_list = self.cleaned_data.get('joining')
        # now check that the group does not exists and create it, rather do this in the form
        qs_shop_group = List.objects.all()
        # TODO make this one step
        this_found = qs_shop_group.filter(Q(name__iexact=target_list))
        if this_found.exists():
            raise ValidationError('That list already exists, please enter another name')
        return target_list

    def clean_purpose(self):
        what_purpose = self.cleaned_data.get('purpose')
        print(f'purpose is {what_purpose}')
        if len(what_purpose) > 0:
            return what_purpose
        else:
            raise ValidationError("Purpose is required")


class ItemForm(forms.ModelForm):
    description = forms.CharField()

    class Meta:
        model = Item
        fields = [
            'description',
            'quantity',
            'to_get_from',
        ]

    def __init__(self, *args, **kwargs):
        """ this limits the selection options to only the active list for the user"""
        list = kwargs.pop('list')
        merchant_list = Merchant.objects.filter(for_group_id=list)
        super().__init__(*args, **kwargs)
        self.fields['to_get_from'].queryset = merchant_list

    def clean_description(self):
        return self.cleaned_data['description'].title()

    def clean_to_get_from(self):
        return self.cleaned_data['to_get_from']

    def clean_quantity(self):
        return self.cleaned_data['quantity']


class MerchantForm(forms.ModelForm):
    """
    For gets driven from the list and will use the list reference
    """
    class Meta:
        model = Merchant
        fields = ['name']


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = MasterList
        fields = ['name', 'purpose']
