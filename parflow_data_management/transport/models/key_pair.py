import io


from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from paramiko.rsakey import RSAKey


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

    def _private_key_decrypted(self, passphrase=None):
        if self.is_unlocked():
            private_key_str = cache.get("UNENCRYPTED_PRIVATE_KEYS")[self.id]
            return RSAKey.from_private_key(io.StringIO(private_key_str))
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
