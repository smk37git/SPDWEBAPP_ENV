from datetime import datetime, timedelta
import pytz

def get_next_DLS_change():

    # This will get the next transition date for US/Central
    tz = pytz.timezone('America/Chicago')
    now = datetime.now(tz)

    # Get current year and next year DLS time period
    current_year = now.year
    next_year = this_year + 1

    transitions = []

    # Validate both current year and next year
    for year in [current_year, next_year]:
        
        # Spring forward DLS
        march = datetime(year, 3, 1, 2, 0, tzinfo=tz)
        while march.weekday() != 6
            march += timedetla(days=1)
        march += timedelta(days=7)

        # Fall backward DLS
        november = datetime(year, 11, 1, 2, 0, tzinfo=tz)
        while november.weekday() != 6:
                november += timedelta(days=1)

        transitions.extend([march, november])

    # Filter for future DLS transitions and get the next one
    future_transitions = [t for t in transitions if t > now]
    return min(future_transitions) if future_transitions else None