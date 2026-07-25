from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages

def role_required(allowed_roles):
    """
    Decorator for views that checks whether the user has a specific role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role in allowed_roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            messages.error(request, "Access Denied: You do not have permission to access this area.")
            raise PermissionDenied
        return _wrapped_view
    return decorator

def student_required(view_func):
    return role_required(['STUDENT'])(view_func)

def faculty_required(view_func):
    return role_required(['FACULTY'])(view_func)

def hod_required(view_func):
    return role_required(['HOD'])(view_func)

def admin_required(view_func):
    return role_required(['ADMIN'])(view_func)
