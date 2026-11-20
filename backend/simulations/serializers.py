from rest_framework import serializers
from .models import SimulationCategory, Simulation, SimulationAttempt, Experiment, ExperimentAttempt


class SimulationCategorySerializer(serializers.ModelSerializer):
    simulation_count = serializers.SerializerMethodField()

    class Meta:
        model = SimulationCategory
        fields = ['id', 'name', 'description', 'subject', 'icon', 'color', 'simulation_count']

    def get_simulation_count(self, obj):
        return obj.simulations.count()


class SimulationSerializer(serializers.ModelSerializer):
    category = SimulationCategorySerializer(read_only=True)

    class Meta:
        model = Simulation
        fields = ['id', 'title', 'description', 'category', 'simulation_type',
                  'difficulty', 'instructions', 'content_data', 'xp_reward', 'thumbnail_url', 'created_at']


class SimulationAttemptSerializer(serializers.ModelSerializer):
    simulation_title = serializers.CharField(source='simulation.title', read_only=True)

    class Meta:
        model = SimulationAttempt
        fields = ['id', 'simulation_title', 'completed', 'score', 'time_spent', 'completed_at']


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ['id', 'title', 'description', 'subject', 'objectives', 'steps', 'expected_results', 'xp_reward', 'created_at']


class ExperimentAttemptSerializer(serializers.ModelSerializer):
    experiment_title = serializers.CharField(source='experiment.title', read_only=True)

    class Meta:
        model = ExperimentAttempt
        fields = ['id', 'experiment_title', 'results_submitted', 'passed', 'xp_earned', 'completed_at']
