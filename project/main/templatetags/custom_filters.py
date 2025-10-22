from django import template

register = template.Library()

@register.filter
def times(value, symbol='★'):
    try:
        return symbol * int(value)
    except (ValueError, TypeError):
        return ''
