from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
import logging
log = logging.getLogger('lista')


def home(request):
    template = 'home.html'
    context = {}
    return render(request, template, context)


def junk(request):
    return HttpResponse(status=444)
