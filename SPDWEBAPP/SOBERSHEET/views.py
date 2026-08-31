from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, Count, Exists, IntegerField, Max, OuterRef, Q, When
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import date

from AUTHENTICATE.models import Brother_Profile
from PARLEYPRO.pp_decorators import requires_role

from .models import SoberSheetSubmission


def get_academic_year_dates(start_year):
    """Academic year runs Jul 1 of start_year through Jun 30 of start_year+1."""
    start = date(start_year, 7, 1)
    end = date(start_year + 1, 6, 30)
    return start, end


def get_available_academic_years(past=3):
    """Last `past` academic years, most recent first."""
    today = timezone.now().date()
    curr_start = today.year - 1 if today.month <= 6 else today.year
    return [curr_start - i for i in range(past)]


@login_required
@requires_role('ACTIVE')
def sober_sheet_dashboard(request):
    required_sober_times = 2
    selected_year = int(request.GET.get('year', (timezone.now().year - 1) if timezone.now().month <= 6 else timezone.now().year))
    start_date, end_date = get_academic_year_dates(selected_year)

    is_risk_manager = request.user.brother_profile.roles.filter(name='RISK_MGR').exists()
    is_prev_risk_manager = request.user.brother_profile.roles.filter(name='PREV_RISK_MGR').exists()
    total_approved_times = SoberSheetSubmission.objects.filter(
        sober_time_approval_status='approved',
        sober_time_date__range=(start_date, end_date),
    ).count()

    user_total_times = SoberSheetSubmission.objects.filter(
        user=request.user,
        sober_time_approval_status='approved',
        sober_time_date__range=(start_date, end_date),
    ).count()

    user_submissions = SoberSheetSubmission.objects.filter(
        user=request.user,
        sober_time_date__range=(start_date, end_date),
    ).order_by('-sober_time_date', '-sober_time_submission_request_date')

    context = {
        'is_risk_manager': is_risk_manager,
        'is_prev_risk_manager': is_prev_risk_manager,
        'total_approved_times': total_approved_times,
        'required_sober_times': required_sober_times,
        'user_total_times': user_total_times,
        'user_submissions': user_submissions,
        'available_years': get_available_academic_years(),
        'selected_year': selected_year,
        'year_label': f"{selected_year}–{selected_year+1} Academic Year",
    }

    if is_risk_manager:
        context['pending_count'] = SoberSheetSubmission.objects.filter(
            sober_time_approval_status='requested',
            sober_time_date__range=(start_date, end_date),
        ).count()

        brother_sober_totals = Brother_Profile.objects.filter(
            roles__name='ACTIVE'
        ).select_related('user').annotate(
            total_times=Count(
                'user__sobersheetsubmission',
                filter=Q(
                    user__sobersheetsubmission__sober_time_approval_status='approved',
                    user__sobersheetsubmission__sober_time_date__range=(start_date, end_date),
                )
            ),
            most_recent_approved_sober_date=Max(
                'user__sobersheetsubmission__sober_time_date',
                filter=Q(
                    user__sobersheetsubmission__sober_time_approval_status='approved',
                    user__sobersheetsubmission__sober_time_date__range=(start_date, end_date),
                ),
            ),
            has_prev_risk_mgr=Exists(
                Brother_Profile.roles.through.objects.filter(
                    brother_profile_id=OuterRef('pk'),
                    role__name='PREV_RISK_MGR',
                )
            ),
        ).annotate(
            recency_sort_bucket=Case(
                When(most_recent_approved_sober_date__isnull=True, then=0),
                default=1,
                output_field=IntegerField(),
            )
        ).distinct().order_by('recency_sort_bucket', 'most_recent_approved_sober_date', 'lastName', 'firstName')

        total_active_members = brother_sober_totals.count()
        members_meeting_goal = sum(
            1 for brother in brother_sober_totals
            if brother.has_prev_risk_mgr or brother.total_times >= required_sober_times
        )

        context['brother_sober_totals'] = brother_sober_totals
        context['total_active_members'] = total_active_members
        context['members_meeting_goal'] = members_meeting_goal
        context['avg_times_per_brother'] = (
            total_approved_times / total_active_members if total_active_members > 0 else 0
        )

    return render(request, 'SOBERSHEET/sober_sheet_dashboard.html', context)


@login_required
@requires_role('ACTIVE')
def sober_sheet_request(request):
    if request.method == 'POST':
        try:
            submission = SoberSheetSubmission(
                user=request.user,
                sober_time_title=request.POST['sober_time_title'],
                sober_time_date=request.POST['sober_time_date'],
                sober_time_approval_status='requested',
            )
            submission.save()
            messages.success(request, 'Sober time submitted successfully!')
            return redirect('sober_sheet_dashboard')
        except Exception as exc:
            messages.error(request, f'Error submitting sober time: {exc}')

    return render(request, 'SOBERSHEET/sober_sheet_request.html')


@login_required
@requires_role('RISK_MGR')
def sober_sheet_approve(request):
    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        action = request.POST.get('action')

        try:
            submission = SoberSheetSubmission.objects.get(id=submission_id)
            if action == 'approve':
                submission.sober_time_approval_status = 'approved'
            elif action == 'deny':
                submission.sober_time_approval_status = 'denied'

            if action in {'approve', 'deny'}:
                submission.sober_time_approver_name = (
                    f"{request.user.brother_profile.firstName} {request.user.brother_profile.lastName}"
                )
                submission.sober_time_submission_approval_date = timezone.now()
                submission.save()
                messages.success(request, f"Submission successfully {'approved' if action == 'approve' else 'denied'}!")
            else:
                messages.error(request, 'Invalid action requested.')
        except SoberSheetSubmission.DoesNotExist:
            messages.error(request, 'Submission not found.')
        except Exception as exc:
            messages.error(request, f'Error processing submission: {exc}')

    pending_submissions = SoberSheetSubmission.objects.filter(
        sober_time_approval_status='requested'
    ).select_related('user', 'user__brother_profile').order_by('-sober_time_date')

    return render(
        request,
        'SOBERSHEET/sober_sheet_approve.html',
        {'pending_submissions': pending_submissions},
    )
