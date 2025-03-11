
def get_timezone_from_offset(offset_seconds):
    """
    Convert a timezone offset in seconds to an IANA timezone identifier.
    This is a best-effort approach that returns a common timezone for the given offset.
    
    Args:
        offset_seconds (int): Timezone offset in seconds from UTC
        
    Returns:
        str: IANA timezone identifier
    """
    # Create a mapping of common offsets to IANA timezone identifiers
    offset_to_timezone = {
        -43200: "Pacific/Midway",       # UTC-12:00
        -39600: "Pacific/Honolulu",     # UTC-11:00
        -36000: "America/Anchorage",    # UTC-10:00
        -32400: "America/Los_Angeles",  # UTC-09:00
        -28800: "America/Los_Angeles",  # UTC-08:00
        -25200: "America/Denver",       # UTC-07:00
        -21600: "America/Chicago",      # UTC-06:00
        -18000: "America/New_York",     # UTC-05:00
        -14400: "America/Halifax",      # UTC-04:00
        -12600: "America/St_Johns",     # UTC-03:30
        -10800: "America/Sao_Paulo",    # UTC-03:00
        -7200: "America/Noronha",       # UTC-02:00
        -3600: "Atlantic/Azores",       # UTC-01:00
        0: "Europe/London",             # UTC+00:00
        3600: "Europe/Paris",           # UTC+01:00
        7200: "Europe/Helsinki",        # UTC+02:00
        10800: "Europe/Moscow",         # UTC+03:00
        12600: "Asia/Tehran",           # UTC+03:30
        14400: "Asia/Dubai",            # UTC+04:00
        16200: "Asia/Kabul",            # UTC+04:30
        18000: "Asia/Karachi",          # UTC+05:00
        19800: "Asia/Kolkata",          # UTC+05:30
        20700: "Asia/Kathmandu",        # UTC+05:45
        21600: "Asia/Dhaka",            # UTC+06:00
        25200: "Asia/Bangkok",          # UTC+07:00
        28800: "Asia/Shanghai",         # UTC+08:00
        32400: "Asia/Tokyo",            # UTC+09:00
        34200: "Australia/Darwin",      # UTC+09:30
        36000: "Australia/Sydney",      # UTC+10:00
        39600: "Pacific/Noumea",        # UTC+11:00
        43200: "Pacific/Auckland",      # UTC+12:00
        45900: "Pacific/Chatham",       # UTC+12:45
        46800: "Pacific/Tongatapu",     # UTC+13:00
    }
    
    # Return the timezone for the exact offset if available
    if offset_seconds in offset_to_timezone:
        return offset_to_timezone[offset_seconds]
    
    # Otherwise, find the closest offset
    closest_offset = min(offset_to_timezone.keys(), key=lambda x: abs(x - offset_seconds))
    return offset_to_timezone[closest_offset]

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
