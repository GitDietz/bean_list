from datetime import date
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect

from .forms import NewListCreateForm, ChecklistForm
from .models import MasterList, MasterCategories, MasterItem
from .utils import in_post

import logging
log = logging.getLogger("info_logger")


@login_required
def add_checklist(request):
    """
    View to create a new checklist
    url: http://127.0.0.1:8000/lists/list_create
    """
    log.info(f'user = {request.user.username}')
    if request.method == "POST":
        form = ChecklistForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.manager = request.user
            new_list.save()
            new_list.members.add(request.user)
            new_list.leaders.add(request.user)

            return HttpResponseRedirect(reverse('lists:user_lists'))
        else:
            log.info(f'Form errors: {form.errors}')
    else:
        form = ChecklistForm()

    template_name = 'list.html'
    context = {
        'title': 'Create Checklist',
        'form': form,
    }
    return render(request, template_name, context)

