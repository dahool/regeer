from django import template
from django.template import Node, Template, Context, NodeList, VariableDoesNotExist, resolve_variable, TemplateSyntaxError
from django.utils.encoding import smart_str
from common.utils.application import is_installed

register = template.Library()

def do_ifinlist(parser, token, negate):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, "%r takes two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
    return IfInListNode(bits[1], bits[2], nodelist_true, nodelist_false, negate)

@register.tag(name='ifinlist')
def ifinlist(parser, token):
    """
    Given an item and a list, check if the item is in the list

    -----
    item = 'a'
    list = [1, 'b', 'a', 4]
    -----
    {% ifinlist item list %}
        Yup, it's in the list
    {% else %}
        Nope, it's not in the list
    {% endifinlist %}
    """
    return do_ifinlist(parser, token, False)

class IfInListNode(Node):
    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __repr__(self):
        return "<IfInListNode>"

    def render(self, context):
        try:
            val1 = resolve_variable(self.var1, context)
        except VariableDoesNotExist:
            val1 = None
        if self.var2.startswith('list='):
            val2 = self.var2[6:-1].split(',')
        else:
            try:
                val2 = resolve_variable(self.var2, context)
            except VariableDoesNotExist:
                val2 = None
        if val1 in val2:
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

@register.tag(name='iftrue')
def iftrue(parser, token):
    '''
    call the given method with the specified arguments.
    
        {% iftrue object.method arg, ... %}
            ....
        {% else %}
            ....
        {% endiftrue %}
        
        {% iftrue object.method arg1=arg1,arg2=arg2 ... %}
            ....
    '''
    
    bits = list(token.split_contents())
    if len(bits) < 2:
        raise TemplateSyntaxError, "%r takes at least two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()
        
    object = bits[1]
    args = []
    kwargs = {}
        
    bits = iter(bits[2:])
    for bit in bits:
        for arg in bit.split(","):
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.strip()
                kwargs[k] = parser.compile_filter(v)
            elif arg:
                args.append(parser.compile_filter(arg))
                                
    return IfTrueNode(object, args, kwargs, nodelist_true, nodelist_false)

class IfTrueNode(Node):
    def __init__(self, object, args, kwargs, nodelist_true, nodelist_false):
        self.object, self.args, self.kwargs = object, args, kwargs
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfTrueNode>"

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
                
        obj_p = self.object.split('.')
        object = '.'.join(obj_p[:-1])
        method = ''.join(obj_p[-1:])
        obj = resolve_variable(object,context)
        func = getattr(obj,method)
        
        if func(*args, **kwargs):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)
        
@register.tag(name='call')
def do_call(parser, token):
    '''
    call the given method with the given arguments and put the result
    in the specified variable
    
        {% call object.method arg1,arg2 as var %}
    '''
    
    bits = list(token.split_contents())
    if len(bits) < 3:
        raise TemplateSyntaxError, "%r takes at least three arguments (%s)" % (bits[0],bits)

    object = bits[1]
    args = []
    kwargs = {}
    asvar = None
        
    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))

    return CallNode(object, args, kwargs, asvar)    

class CallNode(template.Node):
    
    def __init__(self, object, args, kwargs, asvar):
        self.object, self.args, self.kwargs, self.asvar= object, args, kwargs, asvar

    def __repr__(self):
        return "<CallNode>"

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
                
        obj_p = self.object.split('.')
        object = '.'.join(obj_p[:-1])
        method = ''.join(obj_p[-1:])
        obj = resolve_variable(object,context)
        func = getattr(obj,method)
        
        var = func(*args, **kwargs)
        if self.asvar:
            context[self.asvar] = var
            return ''
        else:
            return var
    
@register.tag(name='set')
def do_setas(parser, token):
    '''
    put property as context variable.
    
        {% set object.property as var %}
    '''

    try:
        tag_name, object, n, asvar = token.split_contents()
    except ValueError, e:
        raise TemplateSyntaxError, "%r takes at least three arguments" % token.split_contents()[0]

    return SetAsNode(object, asvar)    

class SetAsNode(template.Node):
    
    def __init__(self, object, asvar):
        self.object, self.asvar = object, asvar

    def __repr__(self):
        return "<SetAsNode>"

    def render(self, context):
        try:
            obj = resolve_variable(self.object, context)
            context[self.asvar] = obj
        except:
            pass
        return ''

@register.tag(name='captureas')
def do_captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)

class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''


class SplitListNode(template.Node):
    def __init__(self, results, cols, new_results):
        self.results, self.cols, self.new_results = results, cols, new_results

    def split_seq(self, results, cols=2):
        start = 0
        for i in xrange(cols):
            stop = start + len(results[i::cols])
            yield results[start:stop]
            start = stop

    def render(self, context):
        context[self.new_results] = self.split_seq(context[self.results], int(self.cols))
        return ''
    
@register.tag(name='multicolumn')
def list_to_columns(parser, token):
    """Parse template tag: {% list_to_colums results as new_results 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "list_to_columns results as new_results 2"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the list_to_columns tag must be 'as'"
    return SplitListNode(bits[1], bits[4], bits[3])

@register.tag(name='agent')
def do_agent(parser, token):
    try:
        tag_name, n, asvar = token.split_contents()
    except ValueError, e:
        raise TemplateSyntaxError, "%r takes at least two arguments" % token.split_contents()[0]

    return AgentNode(asvar)    

class AgentNode(template.Node):
    
    def __init__(self, asvar):
        self.object, self.asvar = object, asvar

    def __repr__(self):
        return "<SetAsNode>"

    def render(self, context):
        agent= resolve_variable('request.META.HTTP_USER_AGENT', context)
        if agent.startswith('Opera'):
            var = 'Opera'
        elif agent.startswith('Mozilla'):
            if agent.count('AppleWebKit'):
                var = 'Safari'
            elif agent.count('KHTML'):
                var = 'KHTML'
            elif agent.count('MSIE'):
                var = 'MSIE'
            else:
                var = 'Firefox'
        context[self.asvar] = var
        return ''
    
    
@register.tag(name='ifmatch')
def do_ifmatch(parser, token):
    
    try:
        tag_name, arg1, arg2 = token.split_contents()
    except ValueError, e:
        raise TemplateSyntaxError, "%r takes at least two arguments" % token.split_contents()[0]    
    end_tag = 'end' + tag_name
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return IfMatchNode(parser.compile_filter(arg1), parser.compile_filter(arg2), nodelist_true, nodelist_false)

class IfMatchNode(Node):
    def __init__(self, arg1, arg2, nodelist_true, nodelist_false):
        self.arg1, self.arg2 = arg1, arg2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return "<IfMatchNode>"

    def render(self, context):
        arg1 = self.arg1.resolve(context)
        arg2 = self.arg2.resolve(context)
        
        if arg1.count(arg2):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)

from django.template.defaulttags import URLNode
from django.conf import settings

@register.tag(name="urlfull")     
def do_urlfull(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    asvar = None
        
    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))
    return URLFullNode(viewname, args, kwargs, asvar)

class URLFullNode(URLNode):
    def render(self, context): 
        url = super(URLFullNode, self).render(context)
        
        if self.asvar:
            url = context[self.asvar]
            context[self.asvar] = 'http://%s%s' % (getattr(settings, 'SITE_DOMAIN'),
                                                   url)
            return ''
        else:
            return 'http://%s%s' % (getattr(settings, 'SITE_DOMAIN'),
                                                   url)

@register.tag(name="switch")
def do_switch(parser, token):
    """
    The ``{% switch %}`` tag compares a variable against one or more values in
    ``{% case %}`` tags, and outputs the contents of the matching block.  An
    optional ``{% else %}`` tag sets off the default output if no matches
    could be found::

        {% switch result_count %}
            {% case 0 %}
                There are no search results.
            {% case 1 %}
                There is one search result.
            {% else %}
                Jackpot! Your search found {{ result_count }} results.
        {% endswitch %}

    Each ``{% case %}`` tag can take multiple values to compare the variable
    against::

        {% switch username %}
            {% case "Jim" "Bob" "Joe" %}
                Me old mate {{ username }}! How ya doin?
            {% else %}
                Hello {{ username }}
        {% endswitch %}
    """
    bits = token.contents.split()
    tag_name = bits[0]
    if len(bits) != 2:
        raise template.TemplateSyntaxError("'%s' tag requires one argument" % tag_name)
    variable = parser.compile_filter(bits[1])

    class BlockTagList(object):
        # This is a bit of a hack, as it embeds knowledge of the behaviour
        # of Parser.parse() relating to the "parse_until" argument.
        def __init__(self, *names):
            self.names = set(names)
        def __contains__(self, token_contents):
            name = token_contents.split()[0]
            return name in self.names

    # Skip over everything before the first {% case %} tag
    parser.parse(BlockTagList('case', 'endswitch'))

    cases = []
    token = parser.next_token()
    got_case = False
    got_else = False
    while token.contents != 'endswitch':
        nodelist = parser.parse(BlockTagList('case', 'else', 'endswitch'))
        
        if got_else:
            raise template.TemplateSyntaxError("'else' must be last tag in '%s'." % tag_name)

        contents = token.contents.split()
        token_name, token_args = contents[0], contents[1:]
        
        if token_name == 'case':
            tests = map(parser.compile_filter, token_args)
            case = (tests, nodelist)
            got_case = True
        else:
            # The {% else %} tag
            case = (None, nodelist)
            got_else = True
        cases.append(case)
        token = parser.next_token()

    if not got_case:
        raise template.TemplateSyntaxError("'%s' must have at least one 'case'." % tag_name)

    return SwitchNode(variable, cases)

class SwitchNode(Node):
    def __init__(self, variable, cases):
        self.variable = variable
        self.cases = cases

    def __repr__(self):
        return "<Switch node>"

    def __iter__(self):
        for tests, nodelist in self.cases:
            for node in nodelist:
                yield node

    def get_nodes_by_type(self, nodetype):
        nodes = []
        if isinstance(self, nodetype):
            nodes.append(self)
        for tests, nodelist in self.cases:
            nodes.extend(nodelist.get_nodes_by_type(nodetype))
        return nodes

    def render(self, context):
        try:
            value_missing = False
            value = self.variable.resolve(context, True)
        except VariableDoesNotExist:
            no_value = True
            value_missing = None
        
        for tests, nodelist in self.cases:
            if tests is None:
                return nodelist.render(context)
            elif not value_missing:
                for test in tests:
                    test_value = test.resolve(context, True)
                    if value == test_value:
                        return nodelist.render(context)
        else:
            return ""
                    
@register.filter
def truncate(value, arg):
    """
    Truncates a string after a given number of chars  
    Argument: Number of chars to truncate after
    """
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    if not isinstance(value, basestring):
        value = str(value)
    if (len(value) > length):
        return value[:length] + "..."
    else:
        return value
    
@register.tag(name="dowith")
def do_with(parser, token):
    """
    Adds a value to the context (inside of this block) for caching and easy
    access.
    This implementation allow to call a method and passing arguments

    For example::

        {% dowith person.some_method arg1,arg2.... as total %}
            {{ total }} object{{ total|pluralize }}
        {% enddowith %}
    """
    bits = list(token.split_contents())
    if len(bits) < 3:
        raise TemplateSyntaxError, "%r takes at least three arguments (%s)" % (bits[0],bits)

    object = bits[1]
    args = []
    kwargs = {}
    asvar = None
        
    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))

    if not asvar:
        raise TemplateSyntaxError, "%r missing target variable" % (bits[0])
        
    nodelist = parser.parse(('enddowith',))
    parser.delete_first_token()
    
    return WithNode(object, args, kwargs, asvar, nodelist)    

class WithNode(Node):

    def __init__(self, object, args, kwargs, asvar, nodelist):
        self.object, self.args, self.kwargs, self.asvar= object, args, kwargs, asvar
        self.nodelist = nodelist

    def __repr__(self):
        return "<WithNode>"

    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        obj_p = self.object.split('.')
        object = '.'.join(obj_p[:-1])
        method = ''.join(obj_p[-1:])
        obj = resolve_variable(object,context)
        func = getattr(obj,method)

        var = func(*args, **kwargs)
        context.push()
        context[self.asvar] = var
        output = self.nodelist.render(context)
        context.pop()
        return output
    
@register.tag(name='ifinstalled')
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
        return "<IfInstalledNode>"

    def render(self, context):
        obj = resolve_variable(self.object,context)
        
        if is_installed(obj):
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false.render(context)            