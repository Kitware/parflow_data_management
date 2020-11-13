from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from parflow_data_management.scheduler.models.mesh import Mesh

class MeshSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesh
        fields = ("id", "project")

class MeshViewSet(ModelViewSet):
    queryset = Mesh.objects.all()

    serializer_class = MeshSerializer
