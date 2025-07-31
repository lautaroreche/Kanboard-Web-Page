import re
from django import template


register = template.Library()

URL_PATTERN = re.compile(
    r'''(?ix)
    \b(
        (?:https?://|www\.)
        [\w\-]+(\.[\w\-]+)+
        (/[^\s<>"]*)?
    |
        [\w\-]+(\.[\w\-]+)+
        (/[^\s<>"]*)?
    )
    '''
)

@register.filter
def is_url_like(value):
    if not value:
        return False
    return bool(URL_PATTERN.search(value))
