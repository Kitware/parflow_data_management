from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from parflow_data_management.scheduler.models.project import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "owner")

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()

    serializer_class = ProjectSerializer
