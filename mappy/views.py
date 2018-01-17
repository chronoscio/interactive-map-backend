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
