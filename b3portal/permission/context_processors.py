from django.utils.functional import lazy
from b3portal.permission.utils import has_server_perm

class PermLookupDict(object):
    def __init__(self, user, server, module_name):
        self.user, self.server, self.module_name = user, server, module_name

    def __repr__(self):
        return str(self.user.get_all_permissions())

    def __getitem__(self, perm_name):
        return has_server_perm(self.user,"%s.%s" % (self.module_name, perm_name), self.server)

    def __nonzero__(self):
        return self.user.has_module_perms(self.module_name)


class PermWrapper(object):
    def __init__(self, user, server):
        self.user = user
        self.server = server
        
    def __getitem__(self, module_name):
        return PermLookupDict(self.user, self.server, module_name)

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("PermWrapper is not iterable.")

def perm(request):
    return {
        'obj_perms': lazy(lambda: PermWrapper(request.user, request.server), PermWrapper)(),
    }
