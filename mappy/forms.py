from django import forms
from django.contrib.auth.models import User,Group
from django.db import models
from .models import State, Shape, Event
from zipfile import ZipFile
from tempfile import mkdtemp
from django.contrib.gis import geos, gdal
from django.contrib.auth.forms import UserCreationForm
import glob
import shutil





class ShapeForm(forms.ModelForm):

    shape_file = forms.FileField(required=False)
    def __init__(self, *args, **kwargs):

        shape_file = forms.FileField()
        return super(ShapeForm, self).__init__(*args, **kwargs)

    def clean(self):
        form_data = self.cleaned_data
        if form_data['shape_file'] == None and form_data['shape'] == None :
            raise forms.ValidationError("You need to have a value in either shape file or shape ")
        return form_data


    def save(self, commit=True):
        modal = super(ShapeForm, self).save(commit=False)
        if not self.cleaned_data['shape_file'] == None:
            shape_file = self.cleaned_data['shape_file']
            working_dir = mkdtemp()
            try:
                shape_zip = ZipFile(shape_file)
                shape_zip.extractall(working_dir)
            except:
                shutil.rmtree(working_dir)
                print("Could not extract zip file.")

            shapes_list = glob.glob(working_dir + '/*.shp')

            try:
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
                    modal.shape = multipoly
            except:
                shutil.rmtree(working_dir)
                print("Error when converting shape file.")

        if commit == True:
            modal.save()
        return modal

    class Meta:
        model = Shape
        exclude = [ ]



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
            try:
                g = Group.objects.get(name='mapper')
            except Group.DoesNotExist:
                pass
            else:
                user.groups.add(g)



    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
