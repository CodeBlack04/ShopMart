from django import template

register = template.Library()

@register.filter(name='initials')
def initials(full_name):
    initials = ''

    for word in full_name.split(' '):
        if word and len(initials) < 3:
            initials += word[0].upper()

    return initials