from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import State, Shape, Event


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class ShapeSerializer(ModelSerializer):
    """
    Shape is in geoJSON format
    """
    class Meta:
        model = Shape
        fields = '__all__'
