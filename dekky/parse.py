# functions for parsing data

def yes_no(raw):
    """Return True if raw is 'yes' and False if raw is 'no'. Raise a ValueError
    for any other value of raw.
    """
    raw = raw.strip()
    if raw == 'yes':
        return True
    elif raw == 'no':
        return False
    else:
        raise ValueError("'" + raw + "' is not either 'yes' or 'no'")
        
def string_val(raw):
    """Return the given string, but stripped of leading and trailing whitespace
    characters.
    """
    return raw.strip()
    
def int_val(raw):
    """Return the value, stripped and parsed into an int."""
    return int(raw.strip())
    
def delimited_list(raw, delimiter):
    """Return the given string split by the delimiter."""
    parts = raw.strip().split(delimiter)
    clean = []
    for p in parts:
        clean.append(string_val(p))