from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Philanthropy_Hours_Event_and_Request
from AUTHENTICATE.models import Brother_Profile, Role
from django.utils import timezone

from PARLEYPRO.pp_decorators import requires_role
import calendar




@login_required
def philanthropy_dashboard(request):
    #import functions to collect context
    from .views_functions import get_semester_dates, get_available_semesters
    from .views_functions import get_user_events_and_total_hours, collect_philanthropy_statistics
    # Get selected semester from query params or default to current
    selected_year = int(request.GET.get('year', timezone.now().year))
    is_spring = request.GET.get('is_spring', str(timezone.now().month <= 6)).lower() == 'true'
    
    # Get date range for selected semester
    start_date, end_date = get_semester_dates(selected_year, is_spring)
    
    # Get all brothers with the 'Active Member' role
    active_brothers = Brother_Profile.objects.filter(
        roles__name='ACTIVE'
    ).select_related('user')
    
    brothers_progress, total_chapter_hours, members_meeting_goal = collect_philanthropy_statistics(active_brothers, start_date, end_date)
    # Calculate averages
    total_active_members = len(active_brothers)
    avg_hours_per_brother = total_chapter_hours / total_active_members if total_active_members > 0 else 0

    # Get user's personal events
    is_philanthropy_chair = request.user.brother_profile.roles.filter(name='PHILANTHROPY_CHAIR').exists()
    user_events = None
    user_total_hours = 0
    
    user_events, user_total_hours = get_user_events_and_total_hours(request,start_date, end_date)  
    # Get available semesters for selection
    available_semesters = get_available_semesters()

    context = {
        'brothers_progress': sorted(brothers_progress, key=lambda x: x['total_hours'], reverse=True),
        'total_chapter_hours': total_chapter_hours,
        'avg_hours_per_brother': avg_hours_per_brother,
        'members_meeting_goal': members_meeting_goal,
        'total_active_members': total_active_members,
        'user_events': user_events,
        'user_total_hours': user_total_hours,
        'is_philanthropy_chair': is_philanthropy_chair,
        'available_semesters': available_semesters,
        'selected_year': selected_year,
        'is_spring': is_spring,
        'semester_label': f"{'Spring' if is_spring else 'Fall'} {selected_year}"
    }
    
    return render(request, 'philanthropy_dashboard.html', context)

@login_required
def philanthropy_request(request):
    if request.method == 'POST':
        try:
            new_event = Philanthropy_Hours_Event_and_Request(
                user=request.user,
                philanthropy_event_title=request.POST['event_title'],
                philanthropy_event_hours=float(request.POST['hours']),
                philanthropy_event_date=request.POST['event_date'],
                philanthropy_approval_status='requested'
            )
            new_event.save()
            messages.success(request, 'Philanthropy hours submitted successfully!')
            return redirect('philanthropy_dashboard')
        except Exception as e:
            messages.error(request, f'Error submitting hours: {str(e)}')
    
    return render(request, 'philanthropy_request.html')

#@requires_role('PHIL_CHAIR','ACTIVE')
@login_required
def philanthropy_approve(request):
    from .views_functions import philanthropy_approval_POST
    
    if request.method == 'POST':
        philanthropy_approval_POST(request)
    # Get pending requests
    pending_requests = Philanthropy_Hours_Event_and_Request.objects.filter(
        philanthropy_approval_status='requested'
    ).select_related('user', 'user__brother_profile').order_by('-philanthropy_event_date')
    
    return render(request, 'philanthropy_approve.html', {'pending_requests': pending_requests})


@login_required
def brother_philanthropy_history(request, user_id):
    from .views_functions import retrieve_individual_brother_history
    try:
        brother = Brother_Profile.objects.select_related('user').get(user_id=user_id)
        
        #grabs and sorts all of the brothers philanthropy history, outputs the total approved hours per semester
        semester_event_totals, lifetime_event_total = retrieve_individual_brother_history(brother, user_id)
        
        
        context = {
            'brother': brother,
            'semester_totals': semester_event_totals,
            'lifetime_total': lifetime_event_total
        }
        
        return render(request, 'philanthropy_brother_history.html', context)
        
    except Brother_Profile.DoesNotExist:
        messages.error(request, 'Brother not found.')
        return redirect('philanthropy_dashboard')
