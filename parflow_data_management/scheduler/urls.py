from django.urls import include, path
from rest_framework import routers
from .rest import project, simulation, mesh, conceptual_model, metadata

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'projects', project.ProjectViewSet)
router.register(r'simulations', simulation.SimulationViewSet)
router.register(r'meshs', mesh.MeshViewSet)
router.register(r'conceptual_models', conceptual_model.ConceptualModelViewSet)
router.register(r'metadatas', metadata.MetadataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]