from django import template

register = template.Library()


@register.filter(name='join_titles')
def join_titles(value, delimiter=', '):
    return delimiter.join([v.title for v in value])
