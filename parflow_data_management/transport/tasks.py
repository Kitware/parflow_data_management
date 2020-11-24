import io
import json

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.contrib.auth import get_user_model
from paramiko.rsakey import RSAKey
from xkcdpass import xkcd_password as xp

from ..consumers import compute_group_for_user
from parflow_data_management.transport.models.key_pair import KeyPair


@shared_task
def generate_key_and_passphrase(user_id, key_pair_id):
    # TODO: Load this once, instead of every time the function is called?
    wordfile = xp.locate_wordfile()
    wordlist = xp.generate_wordlist(wordfile=wordfile)
    passphrase = xp.generate_xkcdpassword(wordlist)

    new_key = RSAKey.generate(bits=4096)
    public_key = new_key.get_base64()
    out_desc = io.StringIO()
    new_key.write_private_key(out_desc, password=passphrase)

    # Update existing model instance
    key_pair = KeyPair.objects.get(pk=key_pair_id)
    key_pair.owner = get_user_model().objects.get(pk=user_id)
    key_pair.public_key = public_key
    key_pair.private_key_encrypted = out_desc.getvalue()
    key_pair.save()

    # Now send across websocket
    data = {"public_key": public_key, "passphrase": passphrase}
    group = compute_group_for_user(user_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {"type": "public.key.with.passphrase", "data": data}
    )


@shared_task
def unlock_key_pair(key_pair_id, passphrase):
    # Retrieve encrypted private key from the database
    key_pair = KeyPair.objects.get(pk=key_pair_id)
    private_key_encrypted = key_pair.private_key_encrypted

    # Attempt decryption
    key_obj = RSAKey.from_private_key(
        io.StringIO(private_key_encrypted), password=passphrase
    )

    # If it succeeded, get the unencrypted private key
    desc = io.StringIO()
    key_obj.write_private_key(desc)
    private_key_decrypted = desc.getvalue()

    # Store unencrypted private key in the cache
    current_dict = cache.get("UNENCRYPTED_PRIVATE_KEYS")
    if current_dict is None:
        current_dict = dict()

    current_dict[key_pair.id] = private_key_decrypted
    cache.set("UNENCRYPTED_PRIVATE_KEYS", current_dict)
