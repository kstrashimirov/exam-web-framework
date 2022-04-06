from django.http import HttpResponse
from django.shortcuts import render


def allowed_groups(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.all():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'errors/wrong_group.html')
        return wrapper
    return decorator
