
def get_query_order(queryset):
    if hasattr(queryset, 'ordered'):
        if queryset.ordered:
            if queryset.query.extra_order_by:
                return queryset.query.extra_order_by[0]
            elif queryset.query.order_by:
                return queryset.query.order_by[0]
            elif queryset.query.model._meta.ordering:
                return queryset.query.model._meta.ordering[0]
    return None