from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


class KeyPair(TimeStampedModel, models.Model):
    name = CharField(_("Name of Key Pair"), blank=True, null=True, max_length=255)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, related_name="key_pairs",
    )
    public_key = CharField(
        _("Public key for ssh connection"), null=True, max_length=4096
    )
    private_key_encrypted = CharField(
        _("Encrypted private key for ssh connection"), null=True, max_length=4096
    )

    def is_unlocked(self):
        private_key_dict = cache.get("UNENCRYPTED_PRIVATE_KEYS")
        return private_key_dict is not None and self.id in private_key_dict
