from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def replace_true_false(value):
    if value:
        value = "<i class='fas fa-check' style='margin-right: 5px; color: green;'</i>"
    else:
        value = "<i class='fas fa-times' style='margin-right: 5px; color: red;'</i>"
    return mark_safe(value)
