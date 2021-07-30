# custom_tags.py
from django import template
register = template.Library()

import datetime

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


def modify_name(value, arg):
    # if arg is first_name: return the first string before space
    if arg == "first_name":
        return value
    # if arg is last_name: return the last string before space
    if arg == "last_name":
        return value
    # if arg is title_case: return the title case of the string
    if arg == "title_case":
        return value.title()
    return value
    
register.filter('modify_name', modify_name)