from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import State, Shape, Event


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class ShapeSerializer(ModelSerializer):
    """
    Shape is in WKT format
    """

    geoJson = SerializerMethodField()


    def get_geoJson(self, obj):
        return obj.shape.json

    class Meta:
        model = Shape
        fields = '__all__'
