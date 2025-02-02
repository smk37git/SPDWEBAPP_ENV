from .models import Philanthropy_Hours_Event_and_Request
from datetime import datetime, date
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum

#views def philanthropy_dashboard(request):
def get_semester_dates(year, is_spring):
    """Helper function to get semester date range"""
    if is_spring:
        start_date = date(year, 1, 1)
        end_date = date(year, 6, 30)
    else:
        start_date = date(year, 7, 1)
        end_date = date(year, 12, 31)
    return start_date, end_date

def get_available_semesters():
    """Get list of available semesters (3 years back)"""
    current_date = timezone.now().date()
    current_year = current_date.year
    is_spring = current_date.month <= 6
    
    semesters = []
    for year in range(current_year, current_year - 3, -1):
        semesters.append({'year': year, 'semester': 'Spring', 'is_spring': True})
        semesters.append({'year': year, 'semester': 'Fall', 'is_spring': False})
    
    # Sort so most recent is first and mark current semester
    semesters.sort(key=lambda x: (x['year'], not x['is_spring']), reverse=True)
    
    # Mark current semester
    for semester in semesters:
        if semester['year'] == current_year and semester['is_spring'] == is_spring:
            semester['current'] = True
            break
    
    return semesters

def get_user_events_and_total_hours(request,start_date, end_date):
        user_events = Philanthropy_Hours_Event_and_Request.objects.filter(
                user=request.user,
                philanthropy_event_date__range=(start_date, end_date)
            ).order_by('-philanthropy_event_date')
            
        user_total_hours = Philanthropy_Hours_Event_and_Request.objects.filter(
                user=request.user,
                philanthropy_approval_status='approved',
                philanthropy_event_date__range=(start_date, end_date)
            ).aggregate(
                total_hours=Sum('philanthropy_event_hours')
            )['total_hours'] or 0
        return user_events, user_total_hours

def collect_philanthropy_statistics(active_brothers, start_date, end_date):
        brothers_progress = []
        total_chapter_hours = 0
        members_meeting_goal = 0

        for brother in active_brothers:
            approved_hours = Philanthropy_Hours_Event_and_Request.objects.filter(
                user=brother.user,
                philanthropy_approval_status='approved',
                philanthropy_event_date__range=(start_date, end_date)
            ).aggregate(
                total_hours=Sum('philanthropy_event_hours')
            )['total_hours'] or 0
            
            brothers_progress.append({
                'user': brother.user,
                'full_name': f"{brother.firstName} {brother.lastName}",
                'total_hours': approved_hours
            })
            
            total_chapter_hours += approved_hours
            if approved_hours >= 5:
                members_meeting_goal += 1
        
        return brothers_progress, total_chapter_hours, members_meeting_goal

# views def philanthropy_approve(request):
def philanthropy_approval_POST(request):
<<<<<<< HEAD
        if request.method == 'POST':
=======
        
>>>>>>> 19d8394 (complete functionality of philanthropy)
            event_id = request.POST.get('event_id')
            action = request.POST.get('action')
            
            try:
                event = Philanthropy_Hours_Event_and_Request.objects.get(id=event_id)
                if action == 'approve':
                    event.philanthropy_approval_status = 'approved'
                    event.philanthropy_event_approver_name = f"{request.user.brother_profile.firstName} {request.user.brother_profile.lastName}"
                    event.philanthropy_event_submission_approval_date = timezone.now()
                elif action == 'deny':
                    event.philanthropy_approval_status = 'denied'
                
                event.save()
                messages.success(request, f'Event successfully {action}d!')
                
            except Philanthropy_Hours_Event_and_Request.DoesNotExist:
                messages.error(request, 'Event not found')
            except Exception as e:
                messages.error(request, f'Error processing request: {str(e)}')

# view def brother_philanthropy_history(request, user_id):
def retrieve_individual_brother_history(brother, user_id):
    '''
    view def brother_philanthropy_history(request, user_id):

    Basically, this goes and grabs all of the events a brother has ever submitted, 
    looks for the events that have been approved, groups them by semester, 
    and pushes it out to be used as context.
    
    '''
    events = Philanthropy_Hours_Event_and_Request.objects.filter(
            user_id=user_id,
            philanthropy_approval_status='approved'
    ).order_by('-philanthropy_event_date')
    
    # Calculate semester totals
    semester_totals = {}
    
    for event in events:
        year = event.philanthropy_event_date.year
        is_spring = event.philanthropy_event_date.month <= 6
        semester_key = f"{'Spring' if is_spring else 'Fall'} {year}"
        
        if semester_key not in semester_totals:
            semester_totals[semester_key] = {
                'total_hours': 0,
                'events': []
            }
        
        semester_totals[semester_key]['total_hours'] += event.philanthropy_event_hours
        semester_totals[semester_key]['events'].append(event)
    
    # Convert to list and sort by most recent semester
    semester_totals = [
        {'semester': k, **v} 
        for k, v in semester_totals.items()
    ]
    semester_totals.sort(key=lambda x: (
        int(x['semester'].split()[-1]), 
        'Spring' in x['semester']
    ), reverse=True)
    
    # Calculate lifetime total
    lifetime_total = sum(item['total_hours'] for item in semester_totals)

    return semester_totals, lifetime_total