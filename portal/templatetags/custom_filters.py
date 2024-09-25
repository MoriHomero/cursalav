# portal/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def extract_parentheses(value):
    try:
        # Extrae el texto entre paréntesis
        return value.split('(')[-1].split(')')[0]
    except IndexError:
        return value
