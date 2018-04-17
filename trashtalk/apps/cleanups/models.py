from datetime import datetime

from django.db import models

from accounts.models import User
from .constants import COUNTRY_CODE_MAP, STATE_CODE_MAP, LocationCategory as category
from .utils import Coordinates


# pylint: disable=missing-docstring
class Cleanup(models.Model):
    DEFAULT_ICON = 'images/defaults/bow_rake.jpg'

    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    image = models.CharField(max_length=300, blank=True, default=DEFAULT_ICON)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cleanups", null=True, blank=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)

    participants = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return "Cleanup at {0}".format(self.location)

    @property
    def gmap_query(self):
        """For street queries."""
        # TODO: Issue #12 - Add cross street queries when implemented.
        if self.location and self.location.cross_street:
            return "{0}:{1}, {2}".format(self.location.street,
                                         self.location.cross_street, self.location.city)
        return self.address

    @property
    def address(self):
        return "{0}+{1},{2}+{3}".format(self.location.street,
                                        self.location.city, self.location.state,
                                        self.location.zipcode)

    def check_name(self):
        # TODO: Refactor as staticmethod; set location as a default on the name field
        if not self.title:
            self.title = self.location

    @property
    def event_start(self):
        """User friendly time. Convert event times to 12-hr format."""
        return datetime.strptime(str(self.start_time), '%X').strftime('%I:%M %p')

    @property
    def event_end(self):
        """User friendly time. Convert event times to 12-hr format."""
        return datetime.strptime(str(self.end_time), '%X').strftime('%I:%M %p')


# pylint: disable=missing-docstring
class Location(models.Model):
    DEFAULT_CITY = "Oakland"
    DEFAULT_STATE = "California"
    DEFAULT_COUNTRY = "United States"
    LOCATION_CATEGORIES = [(category.intersection, 'Intersection'),
                           (category.address, 'Address'),
                           (category.public, 'Public Building'),
                           (category.landnmark, 'Landmark')]

    # Fields with blank=True make them non-required fields
    number = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    cross_street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, default=DEFAULT_CITY)
    state = models.CharField(max_length=100, default=DEFAULT_STATE)
    zipcode = models.CharField(max_length=10, blank=True)
    county = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default=DEFAULT_COUNTRY)
    query_string = models.CharField(max_length=200, null=True, blank=True, help_text='String used to query this location')
    latitude = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=7)
    longitude = models.DecimalField(blank=True, null=True, decimal_places=4, max_digits=7)
    category = models.CharField(choices=LOCATION_CATEGORIES, max_length=100, blank=True, null=True)

    def __str__(self):
        if self.query_string:
            return self.query_string
        return "{0} {1}, {2}".format(self.address, self.city, self.state)

    @property
    def address(self):
        """Provide neatly formatted address."""
        return "{} {}".format(self.number, self.street)

    @property
    def coordinates(self):
        """Provide easy access to coordinates for queries."""
        return Coordinates(self.latitude, self.longitude)

    @property
    def state_code(self):
        """TODO: Set as a default on model field?"""
        if not self.has_state_code():
            return STATE_CODE_MAP[self.state]
        return self.state

    @property
    def country_code(self):
        if not self.has_country_code():
            self.country = COUNTRY_CODE_MAP[self.country]
        return self.country

    def has_country_code(self):
        return len(self.country) < 3

    def has_state_code(self):
        return len(self.state) < 3

    def is_intersection(self):
        return self.category == 'intersection'

# pylint: disable=missing-docstring
class ToolCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "tool categories"

    def __str__(self):
        return self.name

# pylint: disable=missing-docstring
class Tool(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    image_static_location = models.CharField(max_length=200, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(
        ToolCategory,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

# pylint: disable=missing-docstring
class RequiredTools(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE)
    cleanup = models.ForeignKey(Cleanup, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True)

    class Meta:
        unique_together = ('tool', 'cleanup')
        verbose_name_plural = "required tools"

    def __str__(self):
        return "Cleanup: {} / Tool: {} (quantity: {})".format(
            self.cleanup.title, self.tool.name, self.quantity
        )