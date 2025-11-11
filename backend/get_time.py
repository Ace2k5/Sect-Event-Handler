
from datetime import date

def getTime():
    today = date.today()
    day = today.day
    suffix = get_ordinal_suffix(day)
    formatted_dates = []
    
    # Word formats with ordinal suffixes
    formatted_dates.extend([
        today.strftime("%B %Y"),                           # "November 2025"
        today.strftime("%b %Y"),                           # "Nov 2025"
        today.strftime("%B %d %Y"),                        # "November 20 2025"
        today.strftime("%b %d %Y"),                        # "Nov 20 2025"
        today.strftime("%B %d, %Y"),                       # "November 20, 2025"
        today.strftime("%b %d, %Y"),                       # "Nov 20, 2025"
        f"{today.strftime('%B')} {day}{suffix} {today.year}",      # "November 20th 2025"
        f"{today.strftime('%b')} {day}{suffix} {today.year}",       # "Nov 20th 2025"
        f"{today.strftime('%B')} {day}{suffix}, {today.year}",      # "November 20th, 2025"
        f"{today.strftime('%b')} {day}{suffix}, {today.year}",       # "Nov 20th, 2025"
        f"{day}{suffix} {today.strftime('%B %Y')}",                 # "20th November 2025"
        f"{day}{suffix} {today.strftime('%b %Y')}",                 # "20th Nov 2025"
    ])
    
    # Numerical formats
    formatted_dates.extend([
        today.strftime("%Y/%m"),                           # "2025/11"
        today.strftime("%Y-%m"),                           # "2025-11"
        today.strftime("%m/%Y"),                           # "11/2025"
        today.strftime("%m-%Y"),                           # "11-2025"
        today.strftime("%Y/%m/%d"),                        # "2025/11/20"
        today.strftime("%Y-%m-%d"),                        # "2025-11-20"
        today.strftime("%m/%d/%Y"),                        # "11/20/2025"
        today.strftime("%m-%d-%Y"),                        # "11-20-2025"
    ])
    
    return formatted_dates

def get_ordinal_suffix( day):
    """Returns the correct ordinal suffix for a day number"""
    if 11 <= day <= 13:
        return 'th'
    last_digit = day % 10
    if last_digit == 1:
        return 'st'
    elif last_digit == 2:
        return 'nd'
    elif last_digit == 3:
        return 'rd'
    else:
        return 'th'