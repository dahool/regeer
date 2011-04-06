from django import template

register = template.Library()

@register.tag
def current_nav(parser, token):
    import re
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    if len(args) == 2:
        return NavSelectedNode(args[1])
    else:
        return NavSelectedNode(args[1], args[2])

class NavSelectedNode(template.Node):
    def __init__(self, url, style=None):
        self.url = url
        self.style = style

    def render(self, context):
        try:
            path = context['request'].path
            pValue = template.Variable(self.url).resolve(context)
            if (pValue == '/' or pValue == '') and not (path  == '/' or path == ''):
                return ""
            if path.startswith(pValue):
                if self.style:
                    return self.style
                return "current"
        except:
            pass
        return ""
