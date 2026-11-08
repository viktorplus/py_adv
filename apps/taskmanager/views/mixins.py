class BulkCreateMixin:
    """Lets POST accept a JSON list and create several objects at once."""

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data'), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
