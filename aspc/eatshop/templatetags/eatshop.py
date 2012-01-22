from django import template
import datetime

register = template.Library()

@register.inclusion_tag("eatshop/hours_fragment.html")
def format_hours(business):
    """
    Return business hours information with early morning hours
    presented as people would expect (i.e. Mon 4pm-1am instead of
    Mon 4pm-11:59pm + Tues 12am-1am)
    """
    
    almost_midnight = datetime.time(23,59) # end of the day
    midnight = datetime.time(0,0) # beginning of the day
    
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']
    combined = {}
    
    # First, gather 'normal' hour ranges (not beginning at midnight)
    
    for day in weekdays:
        q = {day: True, 'begin__gt': midnight,}
        if business.hours.filter(**q).count():
            dayranges = combined.get(day, []) # get list of ranges to
                                              # append to
            
            raw_ranges = business.hours.filter(**q).values_list('begin', 'end')
            
            for b, e in raw_ranges:
                if e >= almost_midnight: # Clean midnight for display
                    dayranges.append((b, midnight))
                else:
                    dayranges.append((b,e))
            combined[day] = dayranges
    
    for day_idx, day in enumerate(weekdays):
        q = {day: True, 'begin': midnight,}
        
        # If there's no period starting at midnight for this day, skip it
        if not business.hours.filter(**q).count(): continue
        
        # Otherwise, take end of said period and replace midnight end time
        # of previous day (if it exists)
        
        midnight_period = business.hours.filter(**q)[0]
        old_pd = combined[weekdays[day_idx - 1]][-1] # Last pd yesterday
        if old_pd[1] == midnight:
            new_pd = (old_pd[0], midnight_period.end)
            combined[weekdays[day_idx - 1]][-1] = new_pd # Swap in new pd
    
    as_list = [(a, combined.get(a, [])) for a in weekdays]
    total_times = sum([len(ranges) for day, ranges in as_list])
    
    return {"hours": as_list, 'hours_available': total_times > 0,}