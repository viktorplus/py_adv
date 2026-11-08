from rest_framework.pagination import CursorPagination


class CreatedAtCursorPagination(CursorPagination):
    # DRF's default cursor ordering is '-created'; our models use created_at.
    # '-id' keeps the order stable when several rows share the same created_at.
    ordering = ('-created_at', '-id')
