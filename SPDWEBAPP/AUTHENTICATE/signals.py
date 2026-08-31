from django.db.models.signals import m2m_changed
from django.dispatch import receiver


def auto_add_previous_risk_manager(sender, instance, action, pk_set, **kwargs):
    """
    When RISK_MGR is added to a Brother_Profile's roles,
    automatically add PREV_RISK_MGR as well (if not already present).
    """
    from .models import Role

    if action != 'post_add' or not pk_set:
        return

    # Check if any of the newly-added roles is RISK_MGR
    risk_mgr_added = Role.objects.filter(pk__in=pk_set, name='RISK_MGR').exists()
    if not risk_mgr_added:
        return

    # Add PREV_RISK_MGR if the profile doesn't already have it
    prev_role, _ = Role.objects.get_or_create(name='PREV_RISK_MGR')
    if not instance.roles.filter(pk=prev_role.pk).exists():
        instance.roles.add(prev_role)


def connect_signals():
    """Called from AppConfig.ready() to wire up the m2m signal."""
    from .models import Brother_Profile

    m2m_changed.connect(
        auto_add_previous_risk_manager,
        sender=Brother_Profile.roles.through,
    )
