# Żeby to zadziałało, musimy mieć naszą aplikację zarejestrowaną w settings.
from django import template

register = template.Library()


@register.filter
def replace_pipe_with_comma(value):
    return value.replace('|', ", ")
