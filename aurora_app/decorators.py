from functools import wraps
from flask import g, flash, redirect, request


def public(function):
    function.is_public = True
    return function


def need_to_be(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user.role != role:
                flash(u"You can't do that. You don't have permission.")
                return redirect(request.referrer)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
