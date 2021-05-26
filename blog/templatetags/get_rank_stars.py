from django import template

register = template.Library()


@register.filter
def get_rank_stars(value):
    return range(value, 0, -1)
