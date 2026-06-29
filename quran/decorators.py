from django.shortcuts import redirect
from django.contrib import messages
from .models import orderr
def user_not_authenticated(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

def user_is_authenticated(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator
def only_once(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.session.get('only_once', False):
                return redirect(redirect_url)
            else:
                request.session['only_once'] = True
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

def user_is_superuser(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_superuser:
                messages.error(request, "You are cannot to access this!")
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

def user_is_not_subscribe(function=None, redirect_url='plan_list'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator
def user_is_subscribe(function=None, redirect_url='plan_list'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if  not request.user.status=='subscriber_1' and not request.user.status=='subscriber_2' and not request.user.is_superuser :
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

def cannot_make_order(function=None, redirect_url='home'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if orderr.objects.filter(user=request.user).exists():
                messages.error(request, "You have already made an order!")
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator
