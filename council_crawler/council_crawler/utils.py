import hashlib
from dateutil import parser

def url_to_md5(url):
    m = hashlib.md5()
    m.update(url.encode())
    return m.hexdigest()

def parse_date_string(date_string):
    """find a date object in a string containing a date
    """
    date_string = date_string.replace("-", "/")
    try:
        date = parser.parse(date_string, fuzzy=True)
    except ValueError:
        return None
    return date
