from datetime import date
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, redirect

from .forms import NewListCreateForm, ItemForm
    # ItemForm, MerchantForm, ListGroupForm, UsersGroupsForm, NewGroupCreateForm, SupportLogForm
from .models import Item, Merchant, List, Support
from .utils import in_post


import logging
log = logging.getLogger("info_logger")


#  ################################ Utility methods #################################

def get_session_list_choice(request):
    """
    get the list choice from session or set it using the first list this user is in
    handle the odd case when user is not in a group - should not happen outside DEV
    """
    try:
        log.info("get session choice")
        list_active = request.session['list']  # the session can contain value that is no longer in DB
        if list_active != '':
            log.info(f"session value = {list_active}")
            if List.objects.filter(id=list_active).exists():
                return list_active
            else:
                log.info('No such value in DB, new selection required')
                request.session.pop('list')
                return None
        else:
            log.info(f"session NO value for active list = {list_active}")
            return None
    except KeyError:
        log.info(f'no list in session, getting first option from DB')
        list_choices = List.objects.filter(members=request.user)
        if list_choices:
            select_item = list_choices.first().id
            request.session['list'] = select_item
            return select_item
        else:
            return None


def get_user_list_property(request):
    """
    get the list information for the user
    :return: multiple values
    """
    log.info(f"get multiple properties | user = {request.user.username}")
    list_choices = List.objects.filter(members=request.user)
    list_active_no = get_session_list_choice(request)
    active_list_name = List.objects.filter(id=list_active_no).first()
    user_list_options = list_choices.count()
    log.info(f'active list is {active_list_name}')
    return list_choices, user_list_options, list_active_no, active_list_name


def is_user_leader(request, list_no):
    """"to return boolean indicating that the particular user is a leader and can close/delete items"""
    log.info(f"user = {request.user.username}")
    leader_in_group = List.objects.filter(id=list_no).filter(leaders=request.user).first()
    if leader_in_group:
        log.info(f' user is leader')
        return True
    else:
        log.info(f' user is not leader')
        return False

# from listapp.utils import *
# Views related to the lists


#  ################################ LIST #################################
@login_required
def user_lists(request):
    """
    lists associated with a user - as member or manager
    :param request:
    :return:
    """
    log.info(f'user = {request.user.username}')
    managed_list = List.objects.managed_by(request.user)
    member_list = List.objects.member_of(request.user)
    notice = ''
    context = {
        'title': 'Lists you are linked to',
        'managed_list': managed_list,
        'member_list': member_list,
        'notice': notice,
    }
    return render(request, 'user_lists.html', context)


@login_required
def list_detail(request, pk=None, list_obj=None):
    log.info(f'user = {request.user.username}| id = {pk}')
    if pk:
        list_obj = get_object_or_404(List, pk=pk)

    if request.method == "POST":
        form = NewListCreateForm(request.POST, instance=list_obj)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.name = form.cleaned_data['joining']
            new_list.purpose = form.cleaned_data['purpose']
            new_list.manager = request.user
            new_list.save()
            new_list.members.add(request.user)
            new_list.leaders.add(request.user)

            return HttpResponseRedirect(reverse('lists:user_lists'))
        else:
            log.info(f'Form errors: {form.errors}')
    else:
        form = NewListCreateForm(instance=list_obj)  # will be none if new

    template_name = 'list.html'
    log.info(f'Outside Post section')
    context = {
        'title': 'Create or Update List',
        'form': form,
        'notice': '',
    }
    return render(request, template_name, context)


#  ################################ LIST content #################################
@login_required
def items_list_old(request, pk):
    """
    shows the list of unfulfilled items in the particular list
    responds to item cancel requests and item fulfilled requests
    also hands off to the item edit view
    list will only be one the user is a member of
    pk is the pk of the particular list
    """
    # get the active list for the user
    log.info(f"view entry | user = {request.user.username}")
    list_choices = List.objects.filter(members=request.user)
    # if not list_choices:
    #     log.info(f"user has no groups redirect to create?")
    #     return redirect('lists:list_create')
    list_active_no = get_session_list_choice(request)
    # if list_active_no is None:
    #     log.info(f"redirect to group selection | user = {request.user.username}")
    #     redirect('shop:group_select')
    # active_list_name = List.objects.filter(id=list_active_no).first()
    leader_names = list(active_list_name.leaders.all().values_list('username', flat=True))
    # method above to create list: .values('fieldname') will create a tuple with key and value
    lead = ', '.join(leader_names)

    user_list_options = list_choices.count()

    logging.info(f"active list is {active_list_name} | user = {request.user.username}")
    # leader status allows user to see the action buttons and to perform their actions
    leader_status = is_user_leader(request, list_active_no)

    if request.user.is_authenticated:
        queryset_list = Item.objects.to_get_by_group(list_active_no)
        notice = ''
        if request.POST:
            log.info(f"form submitted | user = {request.user.username}")
            log.info(f"which item to purchase or cancel | user = {request.user.username}")
            cancel_item = in_post(request.POST, 'cancel_item')
            purchased_item = in_post(request.POST, 'got_item')

            if cancel_item != 0 or purchased_item != 0:
                item_to_update = max(cancel_item, purchased_item)
                instance = get_object_or_404(Item, id=item_to_update)
                if instance.requested == request.user or leader_status:
                    if cancel_item != 0:
                        log.info(f'to cancel item {cancel_item}')
                        instance.cancelled = request.user
                    elif purchased_item != 0:
                        log.info(f'fulfilled item {purchased_item}')
                        instance.purchased = request.user
                        instance.date_purchased = date.today()
                    instance.save()
            else:
                log.info(f'No objects to update')
        elif request.POST:
            notice = "You can't update the items"
            log.info(f"no permission to update | user = {request.user.username}")

        context = {
            'title': 'Your list',
            'object_list': queryset_list,
            # 'active_list': active_list_name,
            'user_lists': user_list_options,
            'is_leader': leader_status,
            'notice': notice,
            'leader_list': lead,
        }
        return render(request, 'item_list.html', context)
    else:
        raise Http404


@login_required
def items_list(request, pk):
    """
    Manage display of items in the list based on the pk of the list
    :url  http://127.0.0.1:8000/lists/items_list/1
    :param request:
    :param pk: is the list containing the items
    :return:
    """
    log.info(f"view entry | user = {request.user.username}")
    active_list = List.objects.get(pk=pk)
    leader_status = is_user_leader(request, pk)
    if request.user.is_authenticated:
        queryset_list = Item.objects.to_get_by_list(pk)
        notice = ''
        if request.POST:
            log.info(f"form submitted | user = {request.user.username}")
            log.info(f"which item to purchase or cancel | user = {request.user.username}")
            cancel_item = in_post(request.POST, 'cancel_item')
            purchased_item = in_post(request.POST, 'got_item')

            if cancel_item != 0 or purchased_item != 0:
                item_to_update = max(cancel_item, purchased_item)
                instance = get_object_or_404(Item, id=item_to_update)
                if instance.requested == request.user or leader_status:
                    if cancel_item != 0:
                        log.info(f'to cancel item {cancel_item}')
                        instance.cancelled = request.user
                    elif purchased_item != 0:
                        log.info(f'fulfilled item {purchased_item}')
                        instance.purchased = request.user
                        instance.date_purchased = date.today()
                    instance.save()
                    queryset_list = Item.objects.to_get_by_list(pk)
                else:
                    notice = "You can't update the items"
                    log.info(f"no permission to update | user = {request.user.username}")
            else:
                log.info(f'No objects to update')
        #

    context = {
        'title': 'Your list',
        'object_list': queryset_list,
        'active_list': active_list.name,
        'list_pk': pk,
        # 'user_lists': user_list_options,
        'is_leader': leader_status,
        'notice': notice,
        # 'leader_list': lead,
    }
    return render(request, 'item_list.html', context)


def item_create(request, pk):
    """
    :url http://127.0.0.1:8000/lists/item_create/1
    :param request:
    :param pk: the list PK
    :return: back to the list
    """
    logging.info(f"view entered | user = {request.user.username}")
    list_choices, user_list_options, list_active_no, active_list_name = get_user_list_property(request)
    form = ItemForm(request.POST or None, list=list_active_no)
    title = 'Add purchase items'
    notice = ''
    if form.is_valid():
        logging.info(f"form valid | user = {request.user.username}")

        # get the objects still to purchase and check if this new one is among them
        qs_tobuy = Item.objects.to_get()
        item = form.save(commit=False)
        this_found = qs_tobuy.filter(Q(description__iexact=item.description))
        # this needs to be filtered for the particular list and if item is still to get
        for_group = List.objects.filter(id=list_active_no).first()
        if this_found:
            logging.info(f"item exists | user = {request.user.username}")
            notice = 'Already listed : ' + item.description
        else:
            logging.info(f"item will be added | user = {request.user.username}")
            item.in_group = for_group
            item.description = item.description.title()
            item.requested = request.user
            vendor_id = item.to_get_from
            logging.info(f"item saving for vendor = {vendor_id}")
            item.to_get_from = vendor_id  # this_merchant
            item.date_requested = date.today()
            item.save()
            notice = 'Added ' + item.description

        if 'add_one' in request.POST:
            return redirect('lists:items_list', pk=pk)
        else:
            form = ItemForm(None, list=list_active_no)

    context = {
        'title': title,
        'form': form,
        'notice': notice,
        'selected_list': active_list_name,
        'list_pk': for_group.pk,
        'no_of_lists': user_list_options,
    }
    return render(request, 'item_create.html', context)


def item_edit(request, pk):
    """
    :url http://127.0.0.1:8000/lists/item_create/1
    :param request:
    :param pk: the item PK
    :return: back to the list
    """
    logging.info(f"view entered | user = {request.user.username}")
    item = get_object_or_404(Item, pk=pk)
    active_list = item.in_group.id
    user_is_leader = False
    if request.user in item.in_group.leaders.all():
        user_is_leader = True

    if request.user == item.requested or user_is_leader:
        if request.method == "POST":
            logging.info(f"Posted form for {item}")
            form = ItemForm(request.POST, instance=item, list=active_list)
            if form.is_valid():
                logging.info(f"valid form submitted")
                form.save()
                return HttpResponseRedirect(reverse('lists:items_list', kwargs={'pk': active_list}))

        template_name = 'item_detail.html'
        context = {
            'title': 'Update Item',
            'form': ItemForm(instance=item, list=active_list),
            'notice': '',
            'object': item,
        }
        return render(request, template_name, context)
    else:
        logging.info(f"diverting to the list view")
        return redirect('lists:items_list pk=active_list')
