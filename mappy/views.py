"""
I'm doing REST for now, but maybe GraphQL would be a better fit for the frontend?
"""

from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import State, Shape, Event
from .serializers import StateSerializer, ShapeSerializer


class StateViewSet(ReadOnlyModelViewSet):
    serializer_class = StateSerializer
    queryset = State.objects.all()


class ShapeViewSet(ReadOnlyModelViewSet):
    serializer_class = ShapeSerializer
    queryset = Shape.objects.all()

    def get_queryset(self):
        queryset = Shape.objects.all()
        date = self.request.query_params.get('date', None)
        if date is not None:
            queryset = queryset.filter(start_date__lte=date, end_date__gte=date)
        return queryset
