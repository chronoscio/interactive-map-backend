# from django.contrib import admin
from django.contrib.gis import admin
from .models import State, Event, Shape
from .forms import ShapeForm

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Shape)
class ShapeAdmin(admin.OSMGeoAdmin):

    form = ShapeForm

    fields = ('state', 'start_date', 'end_date', 'shape_file', 'shape', 'source', 'start_event', 'end_event')
