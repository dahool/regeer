from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from b3portal.permission import GROUPS

class Command(BaseCommand):
    help = 'Init Permission Groups'

    def handle(self, *args, **options):
        
        for name, perms in GROUPS:
            self.stdout.write("Processing %s...\n" % name)
            g, c = Group.objects.get_or_create(name=name)
            for perm in perms:
                app, model, code = perm.split('.')
                try:
                    p = Permission.objects.get_by_natural_key(code, app, model)
                except:
                    pass
                else:
                    g.permissions.add(p)
                    g.save()
            
        self.stdout.write('Success.\n')
        