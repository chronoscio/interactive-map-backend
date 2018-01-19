from rest_framework.serializers import ModelSerializer

from .models import State, Shape, Event


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('name', 'aliases', 'description', 'color', 'successors')


class ShapeSerializer(ModelSerializer):
    class Meta:
        model = Shape
        fields = ('state', 'shape', 'source', 'start_date', 'start_event', 'end_date', 'end_event')
