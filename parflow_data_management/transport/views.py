from django.http import HttpResponseBadRequest
from django.shortcuts import render
from paramiko import SSHException
from rest_framework.decorators import api_view
from rest_framework.response import Response


from parflow_data_management.transport.tasks import generate_key_and_passphrase
from .models.key_pair import KeyPair
from .models.asset_store import AssetStore


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
    try:
        key_pair.unlock(passphrase)
    except SSHException as e:
        return HttpResponseBadRequest("Invalid passphrase")

    return Response()


def test_ingest_dir(request):
    return render(request, "test_ingest_input_data.html")

@api_view(["POST"])
def asset_store_ingest_dir(request, asset_store_id):
    input_dir = request.data["search_directory"]
    store = AssetStore.objects.filter(pk=asset_store_id)[0]
    store.ingest(input_dir)
    return Response()
