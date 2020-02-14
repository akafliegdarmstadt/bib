from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def stable_get(context, **kwargs):
    get = context['request'].GET.copy()
    for k, v in kwargs.items():
        get[k] = v
    return get.urlencode()


@register.simple_tag(takes_context=True)
def select_sort_class(context, id):
    sort = context['request'].GET.get('sort')

    if sort==id:
        return 'sorted-desc'
    elif sort=='-'+id:
        return 'sorted'
    
    return 'unsorted'