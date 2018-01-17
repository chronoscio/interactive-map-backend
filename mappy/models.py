from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Model, TextField, DateField, ForeignKey, ManyToManyField, CASCADE, SET_NULL
# Never use Charfield. Always use TextField. Postgres treats them the same anyways
# from django.contrib.gis.db.models import PolygonField


class State(Model):
    """
    A State is any cultural/governmental entity that we want to draw on the map.
    It will serve as the foreign key for most other objects.
    We'll start off with a minimal set of fields, we can easily add more if necessary.
    """
    # TODO: Do we want to get rid of aliases and make names their own model?
    # It depends on how we wish to handle state discontinuities like government/name changes.
    # e.g. Do we want to call France something different from 1789-1805? Do we want the Roman Empire
    # to live on as the Byzantine? Am I overthinking this?
    # TODO: On the other end of the spectrum, should we make 'name' the primary key? This could be
    # our desired unique identifier if there are no conflicts
    name = TextField(help_text='Canonical name -- each state should have only one.')
    aliases = TextField(help_text='CSV of alternative names this state may be known by.', blank=True)
    # TODO: Do we need an internal unique country_id for every State? (IMO no)
    # Requiring it would be laborious and cumbersome (we need a consistent hashing schema, and conflict
    # resolution may be controversial). On the other hand, it may be helpful to handle states that
    # go through many name changes
    # country_id = TextField(primary_key=True, help_text='Internal country code for unique internal identification')
    description = TextField(help_text='Links, flavor text, etc.', blank=True)
    successors = ManyToManyField('State', related_name='predecessors', help_text='Successor states')
    # TODO: Should we add an overlord ForeignKey('State')?
    # Not sure how it would work since some states are only temporarily ruled over by others, e.g. Norway
    # Relationships will have to be their own table
    color = TextField(help_text='I expect this to be the most controversial field.')

    def __str__(self):
        return self.name


class Shape(Model):  # Should this just be called Border?
    """
    A Shape is a region polygon associated with a State from a start_date to an end_date.
    This should accomodate States with discontiguous territories and existences.
    A Shape may optionally have Events attached to its start_date and end_date.
    """
    state = ForeignKey(State, on_delete=CASCADE)
    # TODO: Figure out the right way to store the shapefile here. PolygonField feels like the right approach, but is it?
    # Progress! It will probably involve LayerMapping (https://docs.djangoproject.com/en/2.0/ref/contrib/gis/layermapping/)
    # TODO: Add this field once this app is dockerized and Postgres + PostGIS are working
    # shape = PolygonField()
    start_date = DateField(help_text='When this border takes effect.')
    start_event = ForeignKey('Event', on_delete=SET_NULL, null=True, blank=True, related_name='new_borders',
                             help_text="If this field is set, this event's date overwrites the start_date")
    end_date = DateField(help_text='When this border ceases to exist.')
    end_event = ForeignKey('Event', on_delete=SET_NULL, null=True, blank=True, related_name='prior_borders',
                           help_text="If this field is set, this event's date overwrites the end_date")

    def get_bordering_shapes(self, date=None):
        """
        TODO: This property should return the list of shapes that border it at time date.
        If date is None, it should return all shapes thar border it throughout its existence.
        I imagine it will require a custom PostGIS query.
        """
        pass

    def clean(self):
        """
        Sets the start/end_date to the date of the associated events?
        This will need to be called again if the event's date ever changes.
        """
        if self.start_event:
            self.start_date = self.start_event.date
        if self.end_event:
            self.end_date = self.end_event.date

    def __str__(self):
        return f'{self.state}: {self.start_date} to {self.end_date}'


class Event(Model):
    """
    An Event is a date associated with some flavor text and optionally the States affected.
    It may be further associated with a border change via the start_event and end_event in Shapes
    """
    name = TextField(help_text='Canonical name of the event')
    date = DateField()
    # TODO: Add an end_date to simulate ranged events?
    # IMO No, we should only care about events that cause border changes on this map.
    # If a range is ever necessary, just name the event "Start of X" or "End of X"
    states = ManyToManyField('State', help_text='State(s) affected by this event.')
    description = TextField(help_text='Flavor text, Wikipedia, etc.', blank=True)

    def __str__(self):
        return f'{self.name}: {self.date}'


class DiplomaticRelation(Model):
    """
    Abstract class for relationships between states, including wars, alliances, overlordships, etc.
    This is a whole 'nother project that should probably be primarily populated by Wikipedia scraping
    """
    pass
