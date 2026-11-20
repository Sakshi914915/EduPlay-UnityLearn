from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import SimulationCategory, Simulation, SimulationAttempt, Experiment, ExperimentAttempt
from .serializers import (SimulationCategorySerializer, SimulationSerializer,
                           SimulationAttemptSerializer, ExperimentSerializer, ExperimentAttemptSerializer)


class SimulationCategoryListView(generics.ListAPIView):
    queryset = SimulationCategory.objects.all()
    serializer_class = SimulationCategorySerializer
    permission_classes = [AllowAny]


class SimulationListView(generics.ListAPIView):
    serializer_class = SimulationSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['simulation_type', 'difficulty', 'category']
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Simulation.objects.select_related('category').all()


class SimulationDetailView(generics.RetrieveAPIView):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_simulation(request, sim_id):
    """POST /api/simulations/<id>/complete/ - Mark simulation as completed and award XP."""
    simulation = get_object_or_404(Simulation, id=sim_id)
    time_spent = request.data.get('time_spent', 0)
    score = request.data.get('score', 100)

    attempt, created = SimulationAttempt.objects.get_or_create(
        user=request.user, simulation=simulation,
        defaults={'completed': True, 'score': score, 'time_spent': time_spent, 'completed_at': timezone.now()}
    )

    xp_earned = 0
    if created:
        xp_earned = simulation.xp_reward
        profile = request.user.profile
        profile.xp_points += xp_earned
        profile.calculate_level()
        from gamebased.models import XPTransaction
        XPTransaction.objects.create(user=request.user, amount=xp_earned, reason=f'Completed simulation: {simulation.title}')

    return Response({'message': '🎉 Simulation completed!', 'xp_earned': xp_earned, 'first_time': created})


class ExperimentListView(generics.ListAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [AllowAny]
    search_fields = ['title', 'subject']


class ExperimentDetailView(generics.RetrieveAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_experiment(request, exp_id):
    """POST /api/simulations/experiments/<id>/submit/ - Submit experiment results."""
    experiment = get_object_or_404(Experiment, id=exp_id)
    results = request.data.get('results', {})
    passed = request.data.get('passed', True)
    xp_earned = experiment.xp_reward if passed else experiment.xp_reward // 2

    attempt = ExperimentAttempt.objects.create(
        user=request.user, experiment=experiment,
        results_submitted=results, passed=passed, xp_earned=xp_earned
    )

    if xp_earned > 0:
        profile = request.user.profile
        profile.xp_points += xp_earned
        profile.calculate_level()
        from gamebased.models import XPTransaction
        XPTransaction.objects.create(user=request.user, amount=xp_earned, reason=f'Experiment: {experiment.title}')

    return Response({'message': '✅ Experiment submitted!', 'passed': passed, 'xp_earned': xp_earned})
