from django import template


register = template.Library()


@register.filter(name='prettify_currency')
def prettify_currency(value):
    ret = '{:,.2f}'.format(float(value))
    return ret
