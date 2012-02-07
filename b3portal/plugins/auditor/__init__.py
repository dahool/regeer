
def is_enabled(server):
    from b3portal.plugins.auditor.models import AuditLogPlugin
    try:
        AuditLogPlugin.objects.get(server=server)
    except AuditLogPlugin.DoesNotExist:
        return False
    return True