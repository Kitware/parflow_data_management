from django.contrib.postgres.fields import ArrayField
from django.db.models import TextField
from django_extensions.db.models import TimeStampedModel

from .project_asset import ProjectAsset


class Simulation(TimeStampedModel, ProjectAsset):
    arguments = ArrayField(TextField())
