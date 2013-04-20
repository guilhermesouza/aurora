from functools import wraps
from flask import g, flash, redirect, url_for, request


def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in for this page.')
            return redirect(url_for('main.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def need_to_be(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user.role != role:
                flash(u"You can't do that. You don't have permission.")
                print request.referrer
                return redirect(request.referrer)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
