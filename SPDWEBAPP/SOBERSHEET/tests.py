from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from AUTHENTICATE.models import Brother_Profile, Role
from .models import SoberSheetSubmission


class SoberSheetAccessTests(TestCase):
    def setUp(self):
        self.active_role = Role.objects.create(name='ACTIVE')
        self.risk_role = Role.objects.create(name='RISK_MGR')

        self.member = User.objects.create_user(username='member', password='testpass123')
        self.member_profile = Brother_Profile.objects.create(
            user=self.member,
            firstName='Regular',
            lastName='Member',
        )
        self.member_profile.roles.add(self.active_role)

        self.risk = User.objects.create_user(username='risk', password='testpass123')
        self.risk_profile = Brother_Profile.objects.create(
            user=self.risk,
            firstName='Risk',
            lastName='Manager',
        )
        self.risk_profile.roles.add(self.active_role, self.risk_role)

    def test_non_risk_member_can_access_dashboard_but_not_review_page(self):
        SoberSheetSubmission.objects.create(
            user=self.member,
            sober_time_title='Night monitor',
            sober_time_date='2026-08-01',
            sober_time_approval_status='requested',
        )

        self.client.login(username='member', password='testpass123')
        dashboard_response = self.client.get(reverse('sober_sheet_dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, 'Submit Sober Time')
        self.assertContains(dashboard_response, 'Review Pending Submissions')
        self.assertContains(dashboard_response, 'YOUR TOTAL TIMES')
        self.assertContains(dashboard_response, 'Academic Year')
        self.assertContains(dashboard_response, 'Your Submitted Events')
        self.assertContains(dashboard_response, 'Night monitor')
        self.assertContains(dashboard_response, '0/2 times')
        self.assertNotContains(dashboard_response, 'Brotherhood Progress')

        review_response = self.client.get(reverse('sober_sheet_approve'))
        self.assertEqual(review_response.status_code, 302)

    def test_risk_manager_can_review_and_approve_submission(self):
        older_member = User.objects.create_user(username='older', password='testpass123')
        older_profile = Brother_Profile.objects.create(
            user=older_member,
            firstName='Older',
            lastName='Member',
        )
        older_profile.roles.add(self.active_role)

        SoberSheetSubmission.objects.create(
            user=older_member,
            sober_time_title='Old sober monitor',
            sober_time_date='2026-08-01',
            sober_time_approval_status='approved',
        )

        submission = SoberSheetSubmission.objects.create(
            user=self.member,
            sober_time_title='Late-night monitor',
            sober_time_date='2026-08-10',
            sober_time_approval_status='requested',
        )

        self.client.login(username='risk', password='testpass123')
        review_response = self.client.get(reverse('sober_sheet_approve'))
        self.assertEqual(review_response.status_code, 200)
        self.assertContains(review_response, 'Late-night monitor')

        dashboard_response = self.client.get(reverse('sober_sheet_dashboard'))
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, 'Brotherhood Progress')
        self.assertContains(dashboard_response, 'Regular Member')
        self.assertContains(dashboard_response, 'YOUR TOTAL TIMES')
        self.assertContains(dashboard_response, 'Your Submitted Events')
        self.assertContains(dashboard_response, 'Most Recent Approved Sober')

        brother_rows = list(dashboard_response.context['brother_sober_totals'])
        # Risk manager has PREV_RISK_MGR (auto-added by signal) so shows as fulfilled
        risk_row = next(row for row in brother_rows if row.user == self.risk)
        self.assertTrue(risk_row.has_prev_risk_mgr)

        older_row = next(row for row in brother_rows if row.user == older_member)
        self.assertIsNotNone(older_row.most_recent_approved_sober_date)

        approve_response = self.client.post(
            reverse('sober_sheet_approve'),
            {'submission_id': submission.id, 'action': 'approve'},
            follow=True,
        )
        self.assertEqual(approve_response.status_code, 200)

        submission.refresh_from_db()
        self.assertEqual(submission.sober_time_approval_status, 'approved')
        self.assertEqual(submission.sober_time_approver_name, 'Risk Manager')

    def test_prev_risk_manager_has_requirements_fulfilled_on_dashboard(self):
        """Brothers with PREV_RISK_MGR role see 'Requirements Fulfilled' instead of a count."""
        prev_risk_role, _ = Role.objects.get_or_create(name='PREV_RISK_MGR')
        self.member_profile.roles.add(prev_risk_role)

        self.client.login(username='member', password='testpass123')
        response = self.client.get(reverse('sober_sheet_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Requirements Fulfilled')
        self.assertNotContains(response, '0/2 times')

    def test_risk_manager_assignment_auto_adds_prev_risk_manager(self):
        """When RISK_MGR is added to a profile, PREV_RISK_MGR is automatically added."""
        new_user = User.objects.create_user(username='newrisk', password='testpass123')
        new_profile = Brother_Profile.objects.create(
            user=new_user, firstName='New', lastName='Risk',
        )
        new_profile.roles.add(self.active_role)

        # Should not have PREV_RISK_MGR yet
        self.assertFalse(new_profile.roles.filter(name='PREV_RISK_MGR').exists())

        # Adding RISK_MGR should trigger the signal to add PREV_RISK_MGR
        new_profile.roles.add(self.risk_role)
        self.assertTrue(new_profile.roles.filter(name='PREV_RISK_MGR').exists())

    def test_prev_risk_manager_counted_as_meeting_goal_in_brotherhood_progress(self):
        """Brothers with PREV_RISK_MGR are counted as meeting the sober goal in the risk manager's view."""
        prev_risk_role, _ = Role.objects.get_or_create(name='PREV_RISK_MGR')
        self.member_profile.roles.add(prev_risk_role)

        self.client.login(username='risk', password='testpass123')
        response = self.client.get(reverse('sober_sheet_dashboard'))
        self.assertEqual(response.status_code, 200)

        # The member has no approved sobers, but has PREV_RISK_MGR so should count as meeting goal
        self.assertContains(response, 'Requirements Fulfilled')
        # Check context: members_meeting_goal should include the prev risk manager
        self.assertGreaterEqual(response.context['members_meeting_goal'], 1)

    def test_prev_risk_manager_role_name_not_shown_to_users(self):
        """The PREV_RISK_MGR role name itself should never appear in user-facing content."""
        prev_risk_role, _ = Role.objects.get_or_create(name='PREV_RISK_MGR')
        self.member_profile.roles.add(prev_risk_role)

        self.client.login(username='member', password='testpass123')
        response = self.client.get(reverse('sober_sheet_dashboard'))
        self.assertNotContains(response, 'PREV_RISK_MGR')
        self.assertNotContains(response, 'Previous Risk Manager')

