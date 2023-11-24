from django import template

register = template.Library()

@register.filter(name='remove_page_param')
def remove_page_param(query_dict):
    if 'page' in query_dict:
        query_dict = query_dict.copy()
        del query_dict['page']
        
    return query_dict.urlencode()