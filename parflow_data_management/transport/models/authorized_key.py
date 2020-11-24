from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from parflow_data_management.scheduler.models.cluster import Cluster
from parflow_data_management.transport.models.key_pair import KeyPair


# A cluster and a valid public key for a user. Access user through key_pair.
class AuthorizedKey(models.Model):
    cluster = models.ForeignKey(
        Cluster, on_delete=models.CASCADE, related_name="authorized_keys"
    )
    key_pair = models.ForeignKey(
        KeyPair, on_delete=models.CASCADE, related_name="authorized_keys"
    )

    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="authorized_keys"
    )

    username = CharField(_("Username for cluster user"), max_length=30)
