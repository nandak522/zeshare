from django import template

register = template.Library()

@register.inclusion_tag('pagination.html')
def pagination(objects_list):
    previous_page_number = None
    if objects_list.has_previous():
        previous_page_number = objects_list.previous_page_number()
    next_page_number = None
    if objects_list.has_next():
        next_page_number = objects_list.next_page_number()
    current_page_number = objects_list.number
    return {'previous_page_number': previous_page_number,
            'next_page_number': next_page_number,
            'current_page_number': current_page_number}