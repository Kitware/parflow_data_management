from django.urls import path

from . import views

urlpatterns = [
    path("key-generation-test/", views.keygen_view),
    path("keypairs/", views.start_keygen),
    path("keypairs/<int:key_pair_id>/unlock/", views.start_unlock_private_key),
    path("test-unlock-key_pair/", views.test_unlock_private_key),
]