try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.
from django.utils.decorators import available_attrs   
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from common.view.renders.json import render_to_json
#from common.view.renders.xml import render_to_xml

def render(template=None, format=None):
    '''Register response engines based on HTTP_ACCEPT
     
     parameters:
         template: template for html rendering
         format: supported formats ('json','xml')
         
     @render('index.html')
     def my_view(request)

     @render('index.html', ('json','xml'))
     def my_view(request)
          
    html format is supported by default if a template is defined.
    
     @render('json')
     def my_view(request)
    
    in above case, json is the default format.

     @render('json', 'xml')
     def my_view(request)
    
    '''
    
    engines = {}
    default_engine = None

    def __register_engine(engine, template):
        if engine == 'json':
            content_type = 'application/json'
        elif engine == 'html':
            content_type = 'text/html'
        elif engine == 'xml':
            content_type = 'text/xml'
        else:
            raise ValueError("Unsuported format %s" % engine)
        engines[content_type] = engine, template
        return content_type
        
    if format is None:
        format = ()
    elif not isinstance(format, tuple):
        format = (format,)

    if template == 'json':
        default_engine = __register_engine('json', None)
    elif template:
        default_engine = __register_engine('html', template)
        
    for f in format:
        __register_engine(f, None)
    
    def renderer(view_func):
        def _wrapped_view(request, *args, **kwargs):

            def xml_render(request, context):
                #return render_to_xml(context)
                pass
            
            def json_render(request, context):
                return render_to_json(context)
            
            def html_render(request, context, template):
                return render_to_response(
                        template, 
                        context, 
                        context_instance=RequestContext(request),
                    )
            
            context = view_func(request, *args, **kwargs)
            
            if isinstance(context, HttpResponse):
                return context        
            
            engine = None
            
            if request.META.has_key('HTTP_ACCEPT'):
                accept = request.META['HTTP_ACCEPT']
                for content in engines.iterkeys():
                    if accept.find(content)<>-1:
                        engine, template = engines[content] 
                        break
            
            if engine is None:
                # sometimes, for some reason, default_engine is incorret
                if engines.has_key(default_engine):
                    engine, template = engines[default_engine]
                else:
                    engine, template = engines.items()[0]
            
            try:
                cook = context.pop('cookjar',None)
            except:
                pass
    
            try:
                render_template = context.pop('render_template', None)
            except:
                pass
            
            if 'html'==engine:
                if render_template:
                    response = html_render(request, context, render_template)
                else:
                    response = html_render(request, context, template)
            elif 'json'==engine:
                response = json_render(request, context)
            elif 'xml'==engine:
                response = xml_render(request, context)
            else:
                response = context
    
            if isinstance(response, HttpResponse):
                if cook:
                    for k,v in cook.iteritems():
                        if v is None:
                            response.delete_cookie(str(k))
                        else:
                            response.set_cookie(str(k), str(v), getattr(settings, 'COMMON_COOKIE_AGE', None))
            return response
        return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
    return renderer
#
#class render:
#    '''Register response engines based on HTTP_ACCEPT
#     
#     parameters:
#         template: template for html rendering
#         format: supported formats ('json','xml')
#         
#     @render('index.html')
#     def my_view(request)
#
#     @render('index.html', ('json','xml'))
#     def my_view(request)
#          
#    html format is supported by default if a template is defined.
#    
#     @render('json')
#     def my_view(request)
#    
#    in above case, json is the default format.
#
#     @render('json', 'xml')
#     def my_view(request)
#    
#    '''
#    class render_decorator:
#        
#        def __init__(self, parent, view_func):
#            self.parent = parent
#            self.view_func = view_func
#        
#        def __call__(self, *args, **kwargs):
#            request = args[0]    
#            context = self.view_func(*args, **kwargs)
#
#            if isinstance(context, HttpResponse):
#                return context
#            
#            engine = None
#            
#            if request.META.has_key('HTTP_ACCEPT'):
#                accept = request.META['HTTP_ACCEPT']
#                for content in self.parent.engines.iterkeys():
#                    if accept.find(content)<>-1:
#                        engine, template = self.parent.engines.get(content) 
#                        break
#            
#            if engine is None:
#                engine, template = self.parent.engines.get(self.parent.default)
#            
#            cook = context.pop('cookjar',None)
#
#            if 'html'==engine:
#                response = self.html_render(request, context, template)
#            elif 'json'==engine:
#                response = self.json_render(request, context)
#            elif 'xml'==engine:
#                response = self.xml_render(request, context)
#            else:
#                response = context
#
#            if isinstance(response, HttpResponse):
#                if cook:
#                    for k,v in cook.iteritems():
#                        if v is None:
#                            response.delete_cookie(str(k))
#                        else:
#                            response.set_cookie(str(k), str(v), getattr(settings, 'COMMON_COOKIE_AGE', None))
#
#            return response
#            
#        def xml_render(self,request, context):
#            #return render_to_xml(context)
#            pass
#        
#        def json_render(self,request, context):
#            return render_to_json(context)
#        
#        def html_render(self,request, context, template):
#            return render_to_response(
#                template, 
#                context, 
#                context_instance=RequestContext(request),
#            )            
#    
#    def __register_engine(self, engine, template, default = False):
#        
#        if engine == 'json':
#            content_type = 'application/json'
#        elif engine == 'html':
#            content_type = 'text/html'
#        elif engine == 'xml':
#            content_type = 'text/xml'
#        else:
#            raise ValueError("Unsuported format %s" % engine)
#        
#        if default:
#            self.default = content_type
#        self.engines[content_type] = engine, template
#        
#    def __init__(self, template=None, format=None):
#
#        self.engines = {}
#        
#        if format is None:
#            format = ()
#        elif not isinstance(format, tuple):
#            format = (format,)
#
#        if template == 'json':
#            self.__register_engine('json', None, True)
#        elif template:
#            self.__register_engine('html', template, True)
#            
#        for f in format:
#            self.__register_engine(f, None)
#            
#    def __call__(self, view_func):
#        return render.render_decorator(self, view_func)