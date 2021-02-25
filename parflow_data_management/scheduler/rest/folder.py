from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .file import FileSerializer
from parflow_data_management.scheduler.models.file import Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()

    serializer_class = FolderSerializer

    @action(detail=True)
    def content(self, request, pk=None):
        folder = self.get_object()

        folder_serializer = self.get_serializer(folder.folders, many=True)
        file_serializer = FileSerializer(folder.files, many=True)
        return Response(
            {"folders": folder_serializer.data, "files": file_serializer.data}
        )
