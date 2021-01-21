from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from parflow_data_management.scheduler.models.workflow import Workflow

class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = ("id", "project")

class WorkflowViewSet(ModelViewSet):
    queryset = Workflow.objects.all()

    serializer_class = WorkflowSerializer
