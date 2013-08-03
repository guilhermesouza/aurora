from multiprocessing import Process
from functools import wraps

from flask import g, redirect, request, url_for

from .utils import notify, get_session


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
                return redirect(request.args.get('next')
                                or request.referrer
                                or url_for('frontend.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def notify_result(function):
    """Notifies using result from decorated function."""
    @wraps(function)
    def decorated_function(*args, **kwargs):
        result = function(*args, **kwargs)
        notify(**result)
        return function
    return decorated_function


def task(function):
    """Runs function using multiprocessing."""
    def decorated_function(*args, **kwargs):
        process = Process(target=function, args=args + (get_session(),),
                          kwargs=kwargs)

        if function.__name__ == 'deploy':
            from .deployments.views import current_deployments
            deployment_id = str(args[0])
            current_deployments[deployment_id] = process

        process.start()
    return decorated_function
