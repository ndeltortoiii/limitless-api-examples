import datetime
import time
import pytz

def get_timezone_from_offset(offset_seconds):
    """
    Convert a timezone offset in seconds to an IANA timezone identifier.
    This is a best-effort approach that returns a common timezone for the given offset.
    
    Args:
        offset_seconds (int): Timezone offset in seconds from UTC
        
    Returns:
        str: IANA timezone identifier
    """
    # Get current date for DST calculations
    current_date = datetime.datetime.now()
    
    # Dictionary of IANA timezones with their UTC offsets for the current date
    # We'll dynamically calculate the current offset including DST
    timezones = [
        "Pacific/Midway", "Pacific/Honolulu", "America/Anchorage", 
        "America/Los_Angeles", "America/Denver", "America/Chicago", 
        "America/New_York", "America/Halifax", "America/St_Johns",
        "America/Sao_Paulo", "America/Noronha", "Atlantic/Azores",
        "Europe/London", "Europe/Paris", "Europe/Helsinki", 
        "Europe/Moscow", "Asia/Tehran", "Asia/Dubai", 
        "Asia/Kabul", "Asia/Karachi", "Asia/Kolkata", 
        "Asia/Kathmandu", "Asia/Dhaka", "Asia/Bangkok", 
        "Asia/Shanghai", "Asia/Tokyo", "Australia/Darwin",
        "Australia/Sydney", "Pacific/Noumea", "Pacific/Auckland",
        "Pacific/Chatham", "Pacific/Tongatapu"
    ]
    
    # Calculate current offsets for all timezones using pytz
    timezone_offsets = {}
    for tz_name in timezones:
        tz = pytz.timezone(tz_name)
        # Get current offset in seconds for this timezone
        current_offset = int(tz.utcoffset(current_date).total_seconds())
        timezone_offsets[current_offset] = tz_name
    
    # Return the timezone for the exact offset if available
    if offset_seconds in timezone_offsets:
        return timezone_offsets[offset_seconds]
    
    # Otherwise, find the closest offset
    closest_offset = min(timezone_offsets.keys(), key=lambda x: abs(x - offset_seconds))
    return timezone_offsets[closest_offset]

def get_local_timezone():
    """
    Get the local timezone IANA identifier, properly accounting for DST.
    
    Returns:
        str: IANA timezone identifier
    """
    try:
        # First try to use tzlocal if available
        try:
            from tzlocal import get_localzone
            return str(get_localzone())
        except ImportError:
            pass
        
        # Fallback method using time module
        timezone_name = time.tzname[time.daylight if time.localtime().tm_isdst else 0]
        
        # Map common Windows timezone names to IANA
        windows_to_iana = {
            'Eastern Standard Time': 'America/New_York',
            'Central Standard Time': 'America/Chicago',
            'Mountain Standard Time': 'America/Denver',
            'Pacific Standard Time': 'America/Los_Angeles',
            'Alaskan Standard Time': 'America/Anchorage',
            'Hawaiian Standard Time': 'Pacific/Honolulu',
            'GMT Standard Time': 'Europe/London',
            'Central European Standard Time': 'Europe/Budapest',
            'Eastern European Standard Time': 'Europe/Chisinau',
            'China Standard Time': 'Asia/Shanghai',
            'Tokyo Standard Time': 'Asia/Tokyo',
            'AUS Eastern Standard Time': 'Australia/Sydney',
        }
        
        if timezone_name in windows_to_iana:
            return windows_to_iana[timezone_name]
        
        # If we can't map the name, fall back to offset calculation
        local_now = datetime.datetime.now()
        utc_now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        offset_seconds = int((local_now - utc_now).total_seconds())
        return get_timezone_from_offset(offset_seconds)
    
    except Exception as e:
        print(f"Error determining timezone: {e}")
        # Default to UTC if all else fails
        return "UTC"
