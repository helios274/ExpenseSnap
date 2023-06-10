from django import template
from babel import numbers

register = template.Library()

@register.filter
def inr_format(value):
    try:
        float_value = float(value)
    except (TypeError, ValueError):
        return value

    formatted_value = numbers.format_currency(float_value, 'INR', locale="en_IN")

    return formatted_value[1:]
