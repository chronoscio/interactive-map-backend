from django import forms
from django.db import models
from .models import State, Shape, Event
from zipfile import ZipFile
from tempfile import mkdtemp
from django.contrib.gis import geos, gdal
import glob





class ShapeForm(forms.ModelForm):

    shape_file = forms.FileField()
    def __init__(self, *args, **kwargs):

        shape_file = forms.FileField()
        return super(ShapeForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        modal = super(ShapeForm, self).save(commit=False)
        if 'shape_file' in self.cleaned_data:
            shape_file = self.cleaned_data['shape_file']
        working_dir = mkdtemp()
        shape_zip = ZipFile(shape_file)
        shape_zip.extractall(working_dir)

        shapes_list = glob.glob(working_dir + '/*.shp')
        if(len(shapes_list) != 1):
            #error here about having more then one shpaefile on the zip.
            pass
        else:
            ds = gdal.DataSource(shapes_list[0])
            layer = ds[0]
            polygons = []
            for feature in layer:
                state = self.cleaned_data['state']
                geom = feature.geom.geos
                source = self.cleaned_data['source']
                start_date = self.cleaned_data['start_date'] or date(1945, 1, 1)
                end_date = self.cleaned_data['end_date'] or date(2018, 1, 1)

                if type(geom) == geos.Polygon:
                    polygons.append(geom)

            if len(polygons) > 0:
                multipoly = geos.MultiPolygon(polygons)
                modal, created = Shape.objects.get_or_create(state=state, shape=multipoly, source=source, start_date=start_date, end_date=end_date)

            if commit == True:
                m.save()

        return modal

    class Meta:
        model = Shape
        exclude = [ ]
