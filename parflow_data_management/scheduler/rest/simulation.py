from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from parflow_data_management.scheduler.models.simulation import Simulation

class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ("id", "project")

class SimulationViewSet(ModelViewSet):
    queryset = Simulation.objects.all()

    serializer_class = SimulationSerializer
