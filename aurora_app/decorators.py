from multiprocessing import Process
from functools import wraps

from flask import g, redirect, request

from aurora_app.helpers import notify


def public(location):
    """Makes location public"""
    location.is_public = True
    return location


def must_be_able_to(action):
    """Checks if user can do action, if not notifys him and redirects back."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.can(action):
                notify(u"You can't do that. You don't have permission.",
                       category='error', action=action)
                return redirect(request.referrer)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def notify_result(function):
    """Notifies using result from decorated function."""
    def decorated_function(*args, **kwargs):
        result = function(*args, **kwargs)
        notify(**result)
    return decorated_function


def task(function):
    """Runs function using multiprocessing."""
    def decorated_function(*args, **kwargs):
        process = Process(target=function, args=args, kwargs=kwargs)
        process.start()
    return decorated_function
