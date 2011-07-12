from django import template
from django.template import Node, NodeList, resolve_variable, TemplateSyntaxError
from b3portal.plugins import is_plugin_installed

register = template.Library()

@register.tag(name='ifplugininstalled')
def ifinstalled(parser, token):
    '''
    check if the given application is installed.
    '''
    bits = list(token.split_contents())
    if len(bits) < 1:
        raise TemplateSyntaxError, "%r takes at least one argument" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
        
    object = bits[1]
                                
    return IfInstalledNode(object, nodelist_true, nodelist_false)

class IfInstalledNode(Node):
    def __init__(self, object, nodelist_true, nodelist_false):
        self.object, self.nodelist_true, self.nodelist_false = object, nodelist_true, nodelist_false

    def __repr__(self):
        return "<FfPluginInstalledNone>"

    def render(self, context):
        obj = resolve_variable(self.object,context)
        
        if is_plugin_installed(obj):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context) 