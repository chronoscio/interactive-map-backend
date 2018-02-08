# from django.contrib import admin
from django.contrib.gis import admin
from .models import State, Event, Shape
from .forms import ShapeForm
from reversion.admin import VersionAdmin
from reversion_compare.admin import CompareVersionAdmin

@admin.register(State)
class StateAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(CompareVersionAdmin, admin.ModelAdmin):
    pass


@admin.register(Shape)
class ShapeAdmin(CompareVersionAdmin, admin.OSMGeoAdmin):

    form = ShapeForm

    fields = ('state', 'start_date', 'end_date', 'shape_file', 'shape', 'source', 'start_event', 'end_event')
