from datetime import date
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect

from .forms import CustomerForm
from .models import BillingRate, Customer, Invoice, Job, Resource, TimeItem
# from .utils import in_post

import logging
log = logging.getLogger("info_logger")


#  #########  CUSTOMERS  ################
@login_required  # get allow specific users implemented
def customer_all(request):
    """
    list for customer
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    customers = Customer.objects.all().order_by('name')
    notice = ''
    context = {
        'title': 'Customers',
        'objects': customers,
        'notice': notice,
    }
    return render(request, 'customer_list.html', context)


def customer_add(request):
    """
    :url http://127.0.0.1:8000/billing/customer_add
    :param request:
    :return: back to the list
    """
    log.info(f'user = {request.user.username}')
    customers = Customer.objects.all().order_by('name')
    notice = ''
    context = {
        'title': 'Customers',
        'objects': customers,
        'notice': notice,
    }
    return render(request, 'customer_list.html', context)
    #
    # form = CustomerForm(request.POST or None)
    # template = 'customer_create.html'
    # if request.method == "POST":
    #     # log.info(f'from submitted')
    #     if form.is_valid():
    #
    #         item = form.save(commit=False)
    #         item.name = form.cleaned_data['name'].title()
    #         item.save()
    #         return reverse('billing:customer')
    #     else:
    #         # log.info(f'Error on form {form.errors}')
    #         ...
    #
    # template_name = 'merchant.html'
    # context = {
    #     'title': 'Create Merchant',
    #     'form': form,
    #     'notice': '',
    # }
    # return render(request, template, context)


def customer_edit(request, pk):
    ...
#   form reuse
#   validations?


#  #########  Jobs  ################
@login_required  # get allow specific users implemented
def jobs_all(request):
    """
    list for customer
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    customers = Job.objects.all().order_by('name')
    notice = ''
    context = {
        'title': 'Customers',
        'objects': customers,
        'notice': notice,
    }
    return render(request, 'customer_list.html', context)


def customer_add(request):
    ...
    # form, validations, model


def customer_edit(request, pk):
    ...
#   form reuse
#   validations?


#  #########  CUSTOMERS  ################
@login_required  # get allow specific users implemented
def customer_all(request):
    """
    list for customer
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    customers = Customer.objects.all().order_by('name')
    notice = ''
    context = {
        'title': 'Customers',
        'objects': customers,
        'notice': notice,
    }
    return render(request, 'customer_list.html', context)


def customer_add(request):
    ...
    # form, validations, model


def customer_edit(request, pk):
    ...
#   form reuse
#   validations?


#  #########  CUSTOMERS  ################
@login_required  # get allow specific users implemented
def customer_all(request):
    """
    list for customer
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    customers = Customer.objects.all().order_by('name')
    notice = ''
    context = {
        'title': 'Customers',
        'objects': customers,
        'notice': notice,
    }
    return render(request, 'customer_list.html', context)


def customer_add(request):
    ...
    # form, validations, model


def customer_edit(request, pk):
    ...
#   form reuse
#   validations?


#  #########  CUSTOMERS  ################
@login_required  # get allow specific users implemented
def customer_all(request):
    """
    list for customer
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    customers = Customer.objects.all().order_by('name')
    notice = ''
    context = {
        'title': 'Customers',
        'objects': customers,
        'notice': notice,
    }
    return render(request, 'customer_list.html', context)


def customer_add(request):
    ...
    # form, validations, model


def customer_edit(request, pk):
    ...
#   form reuse
#   validations?

