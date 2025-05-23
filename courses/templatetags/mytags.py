from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def previous(pages, current_page):
    """Get the previous page in the sequence"""
    pages_list = list(pages)
    try:
        current_index = pages_list.index(current_page)
        if current_index > 0:
            return pages_list[current_index - 1]
    except (ValueError, IndexError):
        pass
    return None

@register.filter
def next(pages, current_page):
    """Get the next page in the sequence"""
    pages_list = list(pages)
    try:
        current_index = pages_list.index(current_page)
        if current_index < len(pages_list) - 1:
            return pages_list[current_index + 1]
    except (ValueError, IndexError):
        pass
    return None 