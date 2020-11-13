from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from parflow_data_management.scheduler.models.metadata import Metadata

class MetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metadata
        fields = ("id", "project")

class MetadataViewSet(ModelViewSet):
    queryset = Metadata.objects.all()

    serializer_class = MetadataSerializer
