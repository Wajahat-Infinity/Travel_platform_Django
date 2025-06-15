from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from core.settings import LOGIN_REDIRECT_URL


def identity_check_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_REDIRECT_URL):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and not u.is_staff and not u.is_agency and not u.is_buyer and not u.is_completed,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def staff_required_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_REDIRECT_URL):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def vendor_required_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_REDIRECT_URL):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_agency and u.is_completed and not u.is_staff and not u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def customer_required_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_REDIRECT_URL):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda
            u: u.is_active and u.is_completed and not u.is_branch and not u.is_agency and not u.is_staff and not u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def vendor_incomplete_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_REDIRECT_URL):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_agency and not u.is_staff and not u.is_superuser and not u.is_completed,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def branch_incomplete_decorator(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=LOGIN_REDIRECT_URL):
    '''
    Decorator for views that checks that the logged-in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda
            u: u.is_active and u.is_branch and not u.is_staff and not u.is_superuser and not u.is_completed,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
