from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis import geos, gdal

from mappy.models import State, Shape


class Command(BaseCommand):
    help = 'Imports geojson objects with properties: state, source, start_date, end_date'

    def add_arguments(self, parser):
        parser.add_argument('geojson', nargs='+', type=str)

    def handle(self, *args, **options):
        file_names = options['geojson']
        ds = gdal.DataSource(file_names[0])
        layer = ds[0]
        # assert(all(field in layer.fields for field in ['state', 'source', 'start_date', 'end_date']))
        for feature in layer[:2]:
            state = feature.get('name')
            geom = feature.geom.geos
            source = feature.get('source', file_names[0])
            start_date = feature.get('start_date', date(1945, 1, 1))
            if type(geom) == geos.Polygon:
                geom = geos.MultiPolygon(geom)
            qs = State.objects.filter(name=state)
            if qs.count() == 0:
                state = State.objects.create(name=state, color="test")
            elif qs.count() == 1:
                state = qs[0]
            print(state, type(geom))
            Shape.objects.create(state=state, shape=geom, source=source, start_date=start_date, end_date=date(2018, 1, 1))
