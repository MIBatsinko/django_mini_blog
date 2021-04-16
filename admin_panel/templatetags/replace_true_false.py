from django import template


register = template.Library()


@register.filter
def replace_true_false(value):
    if value:
        return '/static/images/true.png'
    else:
        return '/static/images/false.png'
