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
    form = CustomerForm(request.POST or None)
    template = 'customer_create.html'
    if request.method == "POST":
        if form.is_valid():

            item = form.save(commit=False)
            item.name = form.cleaned_data['name'].title()
            item.save()
            return HttpResponseRedirect(reverse('billing:customer'))
        else:
            log.info(f'Error on form {form.errors}')
            ...

    template_name = 'merchant.html'
    context = {
        'title': 'Create Customer',
        'form': form,
        'notice': '',
    }
    return render(request, template, context)


def customer_edit(request, pk):
    log.info(f'user = {request.user.username}')
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    template = 'customer_create.html'
    if request.method == "POST":
        if form.is_valid():

            item = form.save(commit=False)
            item.name = form.cleaned_data['name'].title()
            item.save()
            return HttpResponseRedirect(reverse('billing:customer'))
        else:
            log.info(f'Error on form {form.errors}')
            ...

    template_name = 'merchant.html'
    context = {
        'title': 'Update Customer',
        'form': form,
        'notice': '',
    }
    return render(request, template, context)


#  #########  Jobs  ################
@login_required  # get allow specific users implemented
def jobs_all(request, ck):
    """
    list for customer
    :param ck: customer key
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    template = 'job_list.html'
    list_type = 'all'
    customers = Job.objects.all().order_by('customer').order_by('date_added')
    title = 'All Jobs'
    if int(ck) > 0:
        this_customer = Customer.objects.get(pk=ck)
        customers.filter(customer=this_customer)
        title += f' for {this_customer}'
        list_type = 'customer'
    notice = ''
    context = {
        'title': title,
        'objects': customers,
        'notice': 'notice',
        'list_type': list_type,
    }
    return render(request, template, context)


# def customer_add(request):
#     ...
#     # form, validations, model
#
#
# def customer_edit(request, pk):
#     ...
# #   form reuse
# #   validations?
#
#
# #  #########  CUSTOMERS  ################
# @login_required  # get allow specific users implemented
# def customer_all(request):
#     """
#     list for customer
#     :param request:
#     :return:
#     """
#     log.info(f'user = {request.user.username}')
#     customers = Customer.objects.all().order_by('name')
#     notice = ''
#     context = {
#         'title': 'Customers',
#         'objects': customers,
#         'notice': notice,
#     }
#     return render(request, 'customer_list.html', context)
#
#
# def customer_add(request):
#     ...
#     # form, validations, model
#
#
# def customer_edit(request, pk):
#     ...
# #   form reuse
# #   validations?
#
#
# #  #########  CUSTOMERS  ################
# @login_required  # get allow specific users implemented
# def customer_all(request):
#     """
#     list for customer
#     :param request:
#     :return:
#     """
#     log.info(f'user = {request.user.username}')
#     customers = Customer.objects.all().order_by('name')
#     notice = ''
#     context = {
#         'title': 'Customers',
#         'objects': customers,
#         'notice': notice,
#     }
#     return render(request, 'customer_list.html', context)
#
#
# def customer_add(request):
#     ...
#     # form, validations, model
#
#
# def customer_edit(request, pk):
#     ...
# #   form reuse
# #   validations?
#
#
# #  #########  CUSTOMERS  ################
# @login_required  # get allow specific users implemented
# def customer_all(request):
#     """
#     list for customer
#     :param request:
#     :return:
#     """
#     log.info(f'user = {request.user.username}')
#     customers = Customer.objects.all().order_by('name')
#     notice = ''
#     context = {
#         'title': 'Customers',
#         'objects': customers,
#         'notice': notice,
#     }
#     return render(request, 'customer_list.html', context)
#
#
# def customer_add(request):
#     ...
#     # form, validations, model
#
#
# def customer_edit(request, pk):
#     ...
# #   form reuse
#   validations?

