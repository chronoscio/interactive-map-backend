from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import State, Shape, Event


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        # Must enumerate to display the start_date and end_date because they're properties
        fields = ('id', 'name', 'aliases', 'description', 'successors', 'color', 'start_date', 'end_date')


class ShapeSerializer(ModelSerializer):
    """
    Shape is in geoJSON format
    """
    class Meta:
        model = Shape
        fields = '__all__'
