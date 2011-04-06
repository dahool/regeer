from django import template
from django.conf import settings
from django.template import Node, NodeList, VariableDoesNotExist, resolve_variable, TemplateSyntaxError

register = template.Library()

@register.tag
def setting(parser, token):
    content = token.split_contents()
    asvar = None
    if len(content) == 2:
        tag_name, object = content
    elif len(content) == 4:
        tag_name, object, n, asvar = content
    else:
        raise TemplateSyntaxError, "%r takes at least one argument" % token.split_contents()[0]
    return SettingNode(object, asvar)    

class SettingNode(template.Node):
    
    def __init__(self, object, asvar):
        self.object, self.asvar = object, asvar

    def __repr__(self):
        return "<SettingNode>"

    def render(self, context):
        try:
            obj = resolve_variable(self.object, context)
            res = getattr(settings, obj, '')
            if self.asvar:
                context[self.asvar] = res
            else:
                return res
        except:
            pass
        return ''
    
@register.tag(name='ifsetting')
def ifsetting(parser, token):
    
    try:
        tag, arg = token.split_contents()
    except:
        raise TemplateSyntaxError, "%r takes 1 argument" % token.split_contents()[0]
    end_tag = 'end' + token.split_contents()[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return IfSettingNode(arg, nodelist_true, nodelist_false)

class IfSettingNode(Node):
    def __init__(self, arg, nodelist_true, nodelist_false):
        self.arg = arg
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfSettingNode>"

    def render(self, context):
        try:
            arg = resolve_variable(self.arg, context)
        except VariableDoesNotExist:
            arg = self.arg
        val = getattr(settings, arg, "")
        if val:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)
        