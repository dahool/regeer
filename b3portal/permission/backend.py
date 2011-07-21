
GROUPS = [('Moderator',['b3connect.group.view_group',
                        'b3connect.client.view_client',
                        'b3connect.client.register_client',
                        'b3connect.client.regular_client',
                        'b3connect.client.regular_client',
                        'b3connect.alias.view_aliases',
                        'b3connect.penalty.view_penalty',
                        'b3connect.penalty.view_notices',
                        'b3connect.penalty.view_banlist',
                        'b3connect.penalty.add_notice',
                        'status.serverstatus.view_serverstatus',
                        'follow.follow.view_follow',
                        'chatlog.chatlog.view_chat'])]

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission

class ServerPermissionBackend(ModelBackend):
    
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if obj is None: return False
        if not hasattr(user_obj, '_server_%s_group_perm_cache' % obj.pk):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = []
                serverPerms = user_obj.server_permissions.filter(server=obj)
                for serverPerm in serverPerms:
                    for group in serverPerm.groups.all():
                        perms.extend(group.permissions.values_list('content_type__app_label', 'codename').order_by())
            setattr(user_obj, '_server_%s_group_perm_cache' % obj.pk, set(["%s.%s" % (ct, name) for ct, name in perms]))
        return getattr(user_obj, '_server_%s_group_perm_cache' % obj.pk)

    def get_all_permissions(self, user_obj, obj=None):
        if obj is None: return False
        if not hasattr(user_obj, '_server_%s_perm_cache' % obj.pk):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = set()
                serverPerms = user_obj.server_permissions.filter(server=obj)
                for serverPerm in serverPerms:
                    perms.update(set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in serverPerm.permissions.select_related()]))
                perms.update(self.get_group_permissions(user_obj, obj))
            setattr(user_obj, '_server_%s_perm_cache' % obj.pk, perms)
        return getattr(user_obj, '_server_%s_perm_cache' % obj.pk)

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None: return False
        return perm in self.get_all_permissions(user_obj, obj)
