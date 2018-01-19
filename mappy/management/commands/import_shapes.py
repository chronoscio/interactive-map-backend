from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis import geos, gdal

from mappy.models import State, Shape


class Command(BaseCommand):
    help = 'Imports geojson objects with properties: name, source, start_date, end_date'

    def add_arguments(self, parser):
        parser.add_argument('geojson', nargs='+', type=str)

    def handle(self, *args, **options):
        file_names = options['geojson']
        ds = gdal.DataSource(file_names[0])
        layer = ds[0]
        # assert(all(field in layer.fields for field in ['name', 'start_date', 'end_date']))
        for feature in layer[:2]:
            state = feature.get('name')
            geom = feature.geom.geos
            if type(geom) == geos.Polygon:
                geom = geos.MultiPolygon(geom)
            print(state, type(geom))
