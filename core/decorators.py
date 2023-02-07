from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def check_user_permitted(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            else:
                messages.warning(request,
                                 "You don't have permission for the requested page, Please contact support if this is incorrect")
                return redirect(reverse('home'))

        return wrapper

    return decorator


#
# def check_user_belongs(*lists):
#     def decorator(function):
#         def wrapper(request, *args, **kwargs):
#
#             if request.user.groups.filter(name__in=lists).exists():
#                 return function(request, *args, **kwargs)
#             else:
#                 messages.warning(request, "You don't belong to the requested list")
#                 return redirect(reverse('home'))
#
#         return wrapper
#
#     return decorator