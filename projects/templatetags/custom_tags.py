from django import template


register = template.Library()

@register.filter
def val(d,key):
    return d.get(key)