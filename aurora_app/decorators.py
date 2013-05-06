from functools import wraps
from flask import g, flash, redirect, request


def public(function):
    function.is_public = True
    return function


def must_be_able_to(action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user.can(action):
                flash(u"You can't do that. You don't have permission.")
                return redirect(request.referrer)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
