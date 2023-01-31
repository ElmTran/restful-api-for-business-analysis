from django.shortcuts import get_object_or_404


class BaseMixin(object):
    """Base mixin class for all views."""

    def get_object(self):
        """Get object from database."""
        queryset = self.filter_queryset(self.get_queryset())
        filter = {}
        for field in self.lookup_field:
            if self.kwargs[field]:
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
