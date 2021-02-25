from django.contrib import admin
from .models import asset_store, authorized_key, key_pair

admin.site.register(asset_store.AssetStore)
admin.site.register(authorized_key.AuthorizedKey)
admin.site.register(key_pair.KeyPair)
