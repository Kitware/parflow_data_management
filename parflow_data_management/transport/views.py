import io
import json

from django.core.cache import cache
from django.shortcuts import render
from paramiko.rsakey import RSAKey
from rest_framework.decorators import api_view
from rest_framework.response import Response

from parflow_data_management.transport.tasks import generate_key_and_passphrase
from .models.key_pair import KeyPair


def keygen_view(request):
    return render(request, "basicbutton.html")

def test_unlock_private_key(request):
    return render(request, "test_unlock_page.html")


@api_view(["POST"])
def start_keygen(request):
    # Create an empty row to be populated by the
    # generate_key_and_passphrase function
    key_pair = KeyPair.objects.create()

    # Pass in the ID so we can populate the row
    generate_key_and_passphrase.delay(request.user.id, key_pair.id)

    # Propagate the ID to the user
    return Response(data=str(key_pair.id))


@api_view(["POST"])
def unlock_private_key(request, key_pair_id):
    passphrase = request.data["passphrase"]

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
    return Response()
