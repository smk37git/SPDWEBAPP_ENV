from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from AUTHENTICATE.models import Brother_Profile

def requires_role(role_name):
    """
    Decorator that checks if a user has the specified role.
    If not, redirects to the previous page with an error message.
    
    Usage:
    @requires_role('admin')
    def your_view(request):
        # View logic here
        pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to access this page.")
                return redirect('login')
            
            try:
                brother_profile = Brother_Profile.objects.get(user=request.user)
                # Convert the ManyRelatedManager to a list of values
                user_roles = list(brother_profile.roles.values_list('name', flat=True))
                
                if role_name not in user_roles:
                    messages.error(
                        request, 
                        f"Access denied. You need the '{role_name}' role to access this page."
                    )
                    return redirect('poll')
                    
            except Brother_Profile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('poll')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator