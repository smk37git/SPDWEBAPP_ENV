from django import template
from datetime import datetime, timedelta
from ..utils import get_next_DLS_change
from django import template
from datetime import datetime, timedelta
from ..utils import get_next_DLS_change
from ..models import DayLightSavingsAlert

register = template.Library()

@register.inclusion_tag('MISC/dls_alert.html')
def dls_alert():
    next_change = get_next_DLS_change()
    show_alert = False
    message = ""

    if next_change:
        time_until = next_change - datetime.now(next_change.tzinfo)
        if time_until <= timedelta(days=365):
            show_alert = True
            is_spring = next_change.month == 3
            direction = "forward" if is_spring else "back"
            message = f"Daylight savings Time is on {next_change.strftime('%B %d, %Y')}.\nClocks will move {direction} one hour."

    # Validate if alert is enabled in admin
    try:
        alert_settings = DayLightSavingsAlert.objects.first()
        if alert_settings:
            show_alert = show_alert and alert_settings.is_active
            if alert_settings.name:
                message = alert_settings.name
    except DayLightSavingsAlert.DoesNotExist:
        pass
    
    return {
        'show_alert': show_alert,
        'message': message,
        'next_change': next_change
    }
