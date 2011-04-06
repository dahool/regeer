from django import template

register = template.Library()

@register.inclusion_tag('tags/sorting.html')
def sortheader(data, name, url, style=None):
    if not style:
        style = "sorted"
    if data and data[:1]=="-":
        order = "d"
        data = data[1:]
    else:
        order = "a"
    if url:
        if url.find('?')==-1:
            url = '?' + url
        url += '&'
    else:
        url = "?"
    url += "sort=%s&order=" % name 
    return {'style': style, 'order': order, 'data': data, 'name': name, 'url': url}