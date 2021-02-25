from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from parflow_data_management.scheduler.models.file import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

class FileViewSet(ModelViewSet):
    queryset = File.objects.all()

    serializer_class = FileSerializer
