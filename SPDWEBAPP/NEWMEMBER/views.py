from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .views_functions import *

def newmember_dashboard(request):
    return render(request, 'newmember_dashboard.html')

@login_required
def newmember_marks_dashboard(request):
    new_members = get_new_members()
    new_members_progress = calculate_member_marks(new_members)
    
    is_active = check_user_role(request.user, 'ACTIVE')
    is_new_member = check_user_role(request.user, 'NEW_MEMBER')
    user_submitted_marks = get_user_submitted_marks(request.user) if is_active else None

    # Calculate analytics based on user role
    if is_new_member:
        personal_stats = get_personal_stats(request.user)
        analytics = None
    else:
        analytics = get_active_member_analytics(new_members_progress)
        personal_stats = None
    
    context = {
        'new_members_progress': new_members_progress,
        'user_submitted_marks': user_submitted_marks,
        'is_active': is_active,
        'is_new_member_board': check_user_role(request.user, 'NM_BOARD'),
        'analytics': analytics,
        'personal_stats': personal_stats
    }
    
    template_name = 'ACTIVE_newmember_marks_dashboard.html' if is_active else 'newmember_marks_dashboard.html'
    return render(request, template_name, context)

@login_required
def newmember_request(request):
    if not check_user_role(request.user, 'ACTIVE'):
        messages.error(request, 'Only active members can submit marks.')
        return redirect('newmember_marks_dashboard')
        
    if request.method == 'POST':
        success, message = create_mark_requests(
            requesting_user=request.user,
            target_users=request.POST.getlist('target_users'),
            mark_value=int(request.POST['mark_value']),
            mark_reason=request.POST['mark_reason'],
            mark_date=request.POST['mark_date']
        )
        
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
        return redirect('newmember_marks_dashboard')
    
    new_members = get_new_members()
    return render(request, 'newmember_marks_request.html', {'new_members': new_members})

@login_required
def newmember_approve(request):
    if not check_user_role(request.user, 'NM_BOARD'):
        messages.error(request, 'Only New Member Board members can approve marks.')
        return redirect('newmember_marks_dashboard')
        
    if request.method == 'POST':
        success, message = process_mark_approval(
            request, 
            request.POST.get('mark_id'), 
            request.POST.get('action')
        )
        if success:
            messages.success(request, message)
        else:
            messages.error(request, message)
    
    pending_requests = get_pending_mark_requests()
    
    return render(request, 'newmember_marks_approve.html', {
        'pending_requests': pending_requests
    })

@login_required
def newmember_mark_history(request, user_id):
    try:
        new_member = Brother_Profile.objects.select_related('user').get(
            user_id=user_id,
            roles__name='NEW_MEMBER'
        )
        
        marks, total_marks = get_member_mark_history(user_id)
        
        context = {
            'new_member': new_member,
            'marks': marks,
            'total_marks': total_marks,
            'is_negative': total_marks < 0
        }
        
        return render(request, 'newmember_marks_history.html', context)
        
    except Brother_Profile.DoesNotExist:
        messages.error(request, 'New Member not found.')
        return redirect('newmember_dashboard')