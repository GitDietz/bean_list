from datetime import date
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, redirect

from .forms import MerchantForm
from .models import Merchant, List

import logging
log = logging.getLogger("info_logger")


def is_user_leader(request, list_no):
    """"to return boolean indicating that the particular user is a leader and can close/delete items"""
    logging.info(f"user = {request.user.username}")
    leader_in_group = List.objects.filter(id=list_no).filter(leaders=request.user).first()
    if leader_in_group:
        logging.info(f' user is leader')
        return True
    else:
        logging.info(f' user is not leader')
        return False

#  ################################ Merchant / Supplier #################################


@login_required
def merchant_list(request, pk):
    log.debug('Start')
    active_list = List.objects.get(pk=pk)
    merchants = Merchant.objects.filter(for_group=active_list)
    template = 'merchant_list.html'
    context = {
        'title': f'List of Merchants for the list - {active_list.name}',
        'objects': merchants,
        'list': active_list,
    }
    return render(request, template, context)


@login_required
def merchant_create(request, pk):
    log.debug('Start')
    active_list = List.objects.get(pk=pk)
    form = MerchantForm(request.POST or None)

    template = 'merchant_create.html'
    if form.is_valid():
        logging.info(f"form valid | user = {request.user.username}")

        # check if this new one is already there
        existing_merchants = Merchant.objects.filter(for_group=active_list)
        item = form.save(commit=False)
        this_found = existing_merchants.filter(Q(name__iexact=item.name))
        # this needs to be filtered for the particular list and if merchant doesn't exist
        # for_group = List.objects.filter(id=list_active_no).first()
        if this_found:
            logging.info(f"Merchant exists")
            notice = 'Already listed : ' + item.name
        else:
            logging.info(f"item will be added | user = {request.user.username}")
            item.for_group = active_list
            item.save()
            notice = 'Added ' + item.name
            # now return to merchat list
            return redirect('lists:merchant_list', pk=pk)
    context = {
        'title': f'Add supplier to the list - {active_list.name}',
        'form': form,
        'key': pk,
    }
    return render(request, template, context)


@login_required
def merchant_update(request, pk):
    merchant = get_object_or_404(Merchant, pk=pk)
    list = merchant.for_group
    if request.method == "POST":
        logging.info(f'form submitted')
        form = MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            logging.info(f'complete - direct to list')
            return HttpResponseRedirect(reverse('lists:merchant_list', kwargs={'pk': list.pk}))

    template_name = 'merchant_create.html'
    context = {
        'title': 'Update Merchant',
        'form': MerchantForm(instance=merchant),
        'notice': '',
    }
    return render(request, template_name, context)


@login_required
def merchant_delete(request, pk):
    merchant = get_object_or_404(Merchant, pk=pk)
    list = merchant.for_group
    if is_user_leader(request, list.id):
        notice = ''
    else:
        notice = 'You are not permitted to delete suppliers'
        messages.error(request, notice)  # not sure this is going to work
        return redirect('lists:merchant_list', pk=pk)

    if request.method == 'POST':
        merchant.delete()
        logging.info(f'merchant deleted')
        return HttpResponseRedirect(reverse('lists:merchant_list', kwargs={'pk': list.pk}))

    template_name = 'merchant_delete.html'
    context = {
        'title': 'Delete Merchant',
        'object': merchant,
        'notice': '',
    }
    return render(request, template_name, context)
