from django import template
import datetime
register = template.Library()


@register.filter(name='fromunix')
def fromunix(value):
    return datetime.datetime.fromtimestamp(int(value))


@register.filter(name='to_percent')
def to_percent(value):
    return int(value * 100)
