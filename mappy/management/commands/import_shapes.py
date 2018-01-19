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
        for feature in layer:
            state = feature.get('name')
            geom = feature.geom.geos
            source = 'https://github.com/johan/world.geo.json'
            start_date = feature.get('start_date') or date(1945, 1, 1)
            if type(geom) == geos.Polygon:
                geom = geos.MultiPolygon(geom)
            state, created = State.objects.get_or_create(name=state, color="test")
            print(state, start_date, created)
            Shape.objects.get_or_create(state=state, shape=geom, source=source, start_date=start_date, end_date=date(2018, 1, 1))

        print(State.objects.count())
        print(Shape.objects.count())
