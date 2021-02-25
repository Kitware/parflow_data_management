from django.core import validators
from django.db import models
from django_extensions.db.models import TimeStampedModel

from .project_asset import ProjectAsset
from .folder import Folder
from parflow_data_management.transport.models.asset_store import AssetStore


class File(TimeStampedModel):
    name = models.CharField(
        max_length=255,
        validators=[
            validators.RegexValidator(
                regex="/",
                inverse_match=True,
                message="Name may not contain forward slashes.",
            )
        ],
    )

    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name="files"
    )
    asset_store = models.ForeignKey(
        AssetStore, on_delete=models.CASCADE, related_name="files"
    )

    @property
    def abs_path(self):
        """Get a string representation of this File's absolute path."""
        return f"{self.folder.abs_path}{self.name}"
