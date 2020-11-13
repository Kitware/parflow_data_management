from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from parflow_data_management.scheduler.models.cluster import Cluster


# A cluster and a valid public key for a user.
class AuthorizedKey(models.Model):
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name="authorized_keys")
    public_key = CharField(_("Public key for cluster"), max_length=4096)
