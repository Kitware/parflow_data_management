import io

from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from django.db import models
from django.dispatch import receiver
from django.db.models import TextField
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from paramiko.rsakey import RSAKey


class KeyPair(TimeStampedModel, models.Model):
    name = TextField(_("Name of Key Pair"), blank=True, null=True)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True, related_name="key_pairs",
    )
    public_key = TextField(
        _("Public key for ssh connection"), null=True
    )
    private_key_encrypted = TextField(
        _("Encrypted private key for ssh connection"), null=True
    )

    def is_unlocked(self):
        private_key_dict = cache.get("UNENCRYPTED_PRIVATE_KEYS")
        return private_key_dict is not None and self.id in private_key_dict

    def is_locked(self):
        return not self.is_unlocked()

    def _private_key_decrypted(self):
        if self.is_unlocked():
            return cache.get("UNENCRYPTED_PRIVATE_KEYS")[self.id]
        raise RuntimeError("Private key needs to be unlocked")

    def unlock(self, passphrase):
        if self.is_unlocked():
            return

        # Attempt decryption. Else throws SSHException error.
        key_obj = RSAKey.from_private_key(
            io.StringIO(self.private_key_encrypted), password=passphrase
        )

        # If it succeeded, get the unencrypted private key
        desc = io.StringIO()
        key_obj.write_private_key(desc)
        private_key_decrypted = desc.getvalue()

        # Store unencrypted private key in the cache
        current_dict = cache.get("UNENCRYPTED_PRIVATE_KEYS")
        if current_dict is None:
            current_dict = dict()

        current_dict[self.id] = private_key_decrypted
        cache.set("UNENCRYPTED_PRIVATE_KEYS", current_dict)

    def lock(self):
        if self.is_unlocked():
            key_ids_to_decrypted = cache.get("UNENCRYPTED_PRIVATE_KEYS")
            key_ids_to_decrypted.pop(self.id)
            cache.set("UNENCRYPTED_PRIVATE_KEYS", key_ids_to_decrypted)

# When user logs out, re-lock their keys
@receiver(user_logged_out)
def post_logout(sender, request, user, **kwargs):
    for kp in user.key_pairs.all():
        kp.lock()