from django import template
from django.template import Node, NodeList, resolve_variable, TemplateSyntaxError
from b3portal.plugins import is_plugin_installed, is_plugin_enabled

register = template.Library()

@register.tag(name='ifplugininstalled')
def ifinstalled(parser, token):
    '''
    check if the given plugin is installed.
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
        request = context['request']
        
        server_list = request.server_list
        m = False
        for s in server_list:
            if is_plugin_enabled(s, obj):
                m = True
                break
        
        if m:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context) 

@register.tag(name='ifpluginenabled')
def ifenabled(parser, token):
    '''
    check if the given plugin is enabled.
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

class IfEnabledNode(Node):
    def __init__(self, object, nodelist_true, nodelist_false):
        self.object, self.nodelist_true, self.nodelist_false = object, nodelist_true, nodelist_false

    def __repr__(self):
        return "<FfPluginEnabledNone>"

    def render(self, context):
        obj = resolve_variable(self.object,context)
        request = context['request']

        if is_plugin_enabled(request.server, obj):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)     