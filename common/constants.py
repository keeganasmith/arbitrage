from datetime import datetime, timedelta
import pytz

month_map = {
    "Jan" : 1,
    "Feb" : 2,
    "Mar" : 3,
    "Apr" : 4,
    "May" : 5,
    "Jun" : 6,
    "Jul" : 7,
    "Aug" : 8,
    "Sep" : 9,
    "Oct" : 10,
    "Nov" : 11,
    "Dec" : 12
}
week_map = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6
}
timezone = pytz.timezone('America/Chicago')
def get_date_from_weekday(weekday):
    current_weekday = datetime.now(timezone).weekday
    num_days = weekday - current_weekday
    #weekday = 0, current_weekday = 6, num_days = 1
    if(num_days <= 0):
        num_days += 7
    
    return datetime.now(timezone) + timedelta(days=num_days)
    
    