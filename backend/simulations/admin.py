from django.contrib import admin
from .models import SimulationCategory, Simulation, SimulationAttempt, Experiment, ExperimentAttempt

admin.site.register(SimulationCategory)
admin.site.register(Simulation)
admin.site.register(SimulationAttempt)
admin.site.register(Experiment)
admin.site.register(ExperimentAttempt)
