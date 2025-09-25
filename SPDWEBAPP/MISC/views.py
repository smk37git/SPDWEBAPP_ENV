from django.shortcuts import render

# Create your views here.

# Format the message so that there are linebreaks
message = f"Daylight savings Time is on {next_change.strftime('%B %d, %Y')}. Clocks will move {direction} one hour\n\nClock will move forward an hour"

# Replace newlines with <br> tags to 'copy' a linebreak
message_with_linebreaks = message.replace('\n', '<br>')

# send it back to the message
context = {
    'message': message_with_linebreaks,
    'show_alert': True,
}

return render(request, 'dls_alert.html', context)

