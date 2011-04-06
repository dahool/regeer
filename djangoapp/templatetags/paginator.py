from django import template
from django.conf import settings
import re

register = template.Library()

LEADING_PAGE_RANGE_DISPLAYED = getattr(settings, 'LEADING_PAGE_RANGE_DISPLAYED', 8)
TRAILING_PAGE_RANGE_DISPLAYED = getattr(settings, 'TRAILING_PAGE_RANGE_DISPLAYED', LEADING_PAGE_RANGE_DISPLAYED)
LEADING_PAGE_RANGE = getattr(settings, 'LEADING_PAGE_RANGE', 3)
TRAILING_PAGE_RANGE = getattr(settings, 'TRAILING_PAGE_RANGE', LEADING_PAGE_RANGE)
NUM_PAGES_OUTSIDE_RANGE = getattr(settings, 'PAGES_OUTSIDE_RANGE', 2)
ADJACENT_PAGES = getattr(settings, 'PAGES_OUTSIDE_RANGE', 4)

PAGE_RE = re.compile('[\&]?(page=[0-9]+)')

@register.inclusion_tag('tags/pagination.html')
def paginate(data, params=None):
    return {'data': data, 'params': params}

@register.inclusion_tag('tags/pagination_page.html')
def paginatepage(data, params=None):
    " Initialize variables "
    in_leading_range = in_trailing_range = False
    pages_outside_leading_range = pages_outside_trailing_range = range(0)
 
    context={'pages': data.paginator.num_pages, 'page': data.number}
    
    if (context["pages"] <= LEADING_PAGE_RANGE_DISPLAYED):
        in_leading_range = in_trailing_range = True
        page_numbers = [n for n in range(1, context["pages"] + 1) if n > 0 and n <= context["pages"]]           
    elif (context["page"] <= LEADING_PAGE_RANGE):
        in_leading_range = True
        page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= context["pages"]]
        pages_outside_leading_range = [n + context["pages"] for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
    elif (context["page"] > context["pages"] - TRAILING_PAGE_RANGE):
        in_trailing_range = True
        page_numbers = [n for n in range(context["pages"] - TRAILING_PAGE_RANGE_DISPLAYED + 1, context["pages"] + 1) if n > 0 and n <= context["pages"]]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
    else: 
        page_numbers = [n for n in range(context["page"] - ADJACENT_PAGES, context["page"] + ADJACENT_PAGES + 1) if n > 0 and n <= context["pages"]]
        pages_outside_leading_range = [n + context["pages"] for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]

    if params:
        params = PAGE_RE.sub('',params)
        if params[:1]=="&":
            params = params[1:] 
            
    return {'data': data,
            'numbers': page_numbers,
            'in_leading_range': in_leading_range,
            'page_numbers': page_numbers,
            'pages_outside_trailing_range': pages_outside_trailing_range,
            'in_trailing_range': in_trailing_range,
            'pages_outside_leading_range': pages_outside_leading_range,
            'params': params}