from django_extensions.db.models import TimeStampedModel

from .project_asset import ProjectAsset

class ConceptualModel(TimeStampedModel, ProjectAsset):
    pass
