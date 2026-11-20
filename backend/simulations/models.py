"""
Module 2: Interactive Simulations & Experiments
"""
from django.db import models
from django.contrib.auth.models import User


class SimulationCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    subject = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='🔬')
    color = models.CharField(max_length=7, default='#43E97B')

    class Meta:
        db_table = 'simulation_categories'
        verbose_name_plural = 'Simulation Categories'

    def __str__(self):
        return f"{self.icon} {self.name}"


class Simulation(models.Model):
    SIM_TYPES = [
        ('physics', '⚡ Physics'),
        ('chemistry', '🧪 Chemistry'),
        ('biology', '🧬 Biology'),
        ('math', '📐 Mathematics'),
        ('programming', '💻 Programming'),
    ]
    DIFFICULTY = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(SimulationCategory, on_delete=models.CASCADE, related_name='simulations')
    simulation_type = models.CharField(max_length=20, choices=SIM_TYPES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY, default='medium')
    instructions = models.TextField()
    content_data = models.JSONField(default=dict, help_text='Simulation configuration data')
    xp_reward = models.IntegerField(default=75)
    thumbnail_url = models.URLField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'simulations'

    def __str__(self):
        return f"{self.title} [{self.simulation_type}]"


class SimulationAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulation_attempts')
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='attempts')
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    time_spent = models.IntegerField(default=0, help_text='Seconds spent')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'simulation_attempts'


class Experiment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    objectives = models.TextField()
    steps = models.JSONField(default=list, help_text='List of experiment steps')
    expected_results = models.TextField()
    xp_reward = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'experiments'

    def __str__(self):
        return self.title


class ExperimentAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiment_attempts')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='attempts')
    results_submitted = models.JSONField(default=dict)
    passed = models.BooleanField(default=False)
    xp_earned = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'experiment_attempts'
