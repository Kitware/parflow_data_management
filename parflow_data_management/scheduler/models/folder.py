from django.db import models
from django_extensions.db.models import TimeStampedModel

from .project_asset import ProjectAsset
from parflow_data_management.transport.models.asset_store import AssetStore


class Folder(TimeStampedModel):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="folders",
    )

    asset_store = models.ForeignKey(
        AssetStore, on_delete=models.CASCADE, related_name="folders"
    )

    abs_path = models.CharField(max_length=255)
