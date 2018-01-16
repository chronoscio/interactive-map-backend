from django.contrib import admin
from .models import State, Event, Shape


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    pass
