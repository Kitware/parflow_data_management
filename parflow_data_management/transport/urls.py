from django.urls import path

from .views import (
    asset_store_ingest_dir,
    keygen_view,
    start_keygen,
    test_unlock_private_key,
    test_ingest_dir,
    unlock_private_key,
)

urlpatterns = [
    # Key generation and unlocking
    path("key-generation-test/", keygen_view),
    path("keypairs/", start_keygen),
    path("keypairs/<int:key_pair_id>/unlock/", unlock_private_key),
    path("test-unlock-key_pair/", test_unlock_private_key),
    # Ingesting input data for a simulation using an asset_store
    path("test-ingest-data", test_ingest_dir,),
    path("asset-stores/<int:asset_store_id>/ingest/", asset_store_ingest_dir,),
]
