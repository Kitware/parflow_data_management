from django.contrib import admin
from .models import cluster, conceptual_model, mesh, metadata, project, simulation

admin.site.register(cluster.Cluster)
admin.site.register(conceptual_model.ConceptualModel)
admin.site.register(mesh.Mesh)
admin.site.register(metadata.Metadata)
admin.site.register(project.Project)
admin.site.register(simulation.Simulation)
