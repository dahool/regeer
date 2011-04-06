# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import widgets
from django import forms, template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.admin.filterspecs import FilterSpec
from django.utils.functional import update_wrapper

from b3connect.models import *
from b3connect.filters import DateIntFieldFilterSpec
from b3connect.fields import EpochDateTimeField

FilterSpec.filter_specs.insert(0, (lambda f: isinstance(f, EpochDateTimeField), DateIntFieldFilterSpec))

class CustomModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        EpochDateTimeField: {
            'form_class': forms.SplitDateTimeField,
            'widget': widgets.AdminSplitDateTime
        },
    }

    def get_model_perms(self, request):
        """
        Returns a dict of all perms for this model. This dict has the keys
        ``add``, ``change``, and ``delete`` mapping to the True/False for each
        of those actions.
        """
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request),
        }
        
    def has_view_permission(self, request):
        "Returns True if the given request has permission to add an object."
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' + self.get_view_permission(self.opts.object_name.lower()))

    def get_view_permission(self, name):
        return 'view_%s' % name

    def changelist_view(self, request, extra_context=None):
        "The 'change list' admin view for this model."
        from django.contrib.admin.views.main import ChangeList, ERROR_FLAG
        from django.utils.encoding import force_unicode
        from django.utils.translation import ungettext
        opts = self.model._meta
        app_label = opts.app_label
        
        if not self.has_view_permission(request) or not self.has_change_permission(request, None):
            raise admin.options.PermissionDenied

        # Check actions to see if any are available on this changelist
        actions = self.get_actions(request)

        # Remove action checkboxes if there aren't any actions available.
        list_display = list(self.list_display)
        if not actions:
            try:
                list_display.remove('action_checkbox')
            except ValueError:
                pass

        try:
            cl = ChangeList(request, self.model, list_display, self.list_display_links, self.list_filter,
                self.date_hierarchy, self.search_fields, self.list_select_related, self.list_per_page, self.list_editable, self)
        except admin.options.IncorrectLookupParameters:
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given and
            # the 'invalid=1' parameter was already in the query string, something
            # is screwed up with the database, so display an error page.
            if ERROR_FLAG in request.GET.keys():
                return render_to_response('admin/invalid_setup.html', {'title': _('Database error')})
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        # If the request was POSTed, this might be a bulk action or a bulk edit.
        # Try to look up an action first, but if this isn't an action the POST
        # will fall through to the bulk edit check, below.
        if actions and request.method == 'POST':
            response = self.response_action(request, queryset=cl.get_query_set())
            if response:
                return response

        # If we're allowing changelist editing, we need to construct a formset
        # for the changelist given all the fields to be edited. Then we'll
        # use the formset to validate/process POSTed data.
        formset = cl.formset = None

        # Handle POSTed bulk-edit data.
        if request.method == "POST" and self.list_editable:
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(request.POST, request.FILES, queryset=cl.result_list)
            if formset.is_valid():
                changecount = 0
                for form in formset.forms:
                    if form.has_changed():
                        obj = self.save_form(request, form, change=True)
                        self.save_model(request, obj, form, change=True)
                        form.save_m2m()
                        change_msg = self.construct_change_message(request, form, None)
                        self.log_change(request, obj, change_msg)
                        changecount += 1

                if changecount:
                    if changecount == 1:
                        name = force_unicode(opts.verbose_name)
                    else:
                        name = force_unicode(opts.verbose_name_plural)
                    msg = ungettext("%(count)s %(name)s was changed successfully.",
                                    "%(count)s %(name)s were changed successfully.",
                                    changecount) % {'count': changecount,
                                                    'name': name,
                                                    'obj': force_unicode(obj)}
                    self.message_user(request, msg)

                return HttpResponseRedirect(request.get_full_path())

        # Handle GET -- construct a formset for display.
        elif self.list_editable:
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(queryset=cl.result_list)

        # Build the list of media to be used by the formset.
        if formset:
            media = self.media + formset.media
        else:
            media = self.media

        # Build the action form and populate it with available actions.
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
        else:
            action_form = None

        context = {
            'title': cl.title,
            'is_popup': cl.is_popup,
            'cl': cl,
            'media': media,
            'has_add_permission': self.has_add_permission(request),
            'root_path': self.admin_site.root_path,
            'app_label': app_label,
            'action_form': action_form,
            'actions_on_top': self.actions_on_top,
            'actions_on_bottom': self.actions_on_bottom,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.change_list_template or [
            'admin/%s/%s/change_list.html' % (app_label, opts.object_name.lower()),
            'admin/%s/change_list.html' % app_label,
            'admin/change_list.html'
        ], context, context_instance=context_instance)
                            
class ClientAdmin(CustomModelAdmin):
    search_fields=['=id','name','guid','ip','aliases__alias']
    list_display=('id', 'name', 'displayGroup')
    list_filter=('group',)
    #list_editable=('group',)
    
class AliasAdmin(CustomModelAdmin):
    search_fields=['=client__id','client__name','alias', 'ip']

class PenaltyAdmin(CustomModelAdmin):
    search_fields=['=client__id','client__ip','type','client__name','keyword','reason']
    list_filter=('type',)
    raw_id_fields=('client','admin')

class NickAdmin(CustomModelAdmin):
    search_fields=['=client__id','client__name','name']

class DisabledCommandAdmin(CustomModelAdmin):
    search_fields=['cmd']
            
class GroupAdmin(CustomModelAdmin):
    pass

class AuditAdmin(CustomModelAdmin):
    search_fields=['=client__id','data']
    list_filter=('command',)
    list_display=('command', 'client', 'data', 'time_add')

admin.site.register(Client, ClientAdmin)
admin.site.register(Alias, AliasAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Penalty, PenaltyAdmin)
admin.site.register(Nick, NickAdmin)
admin.site.register(DisabledCommand, DisabledCommandAdmin)
admin.site.register(AuditLog, AuditAdmin)

