from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.SimulationCategoryListView.as_view(), name='sim-categories'),
    path('', views.SimulationListView.as_view(), name='sim-list'),
    path('<int:pk>/', views.SimulationDetailView.as_view(), name='sim-detail'),
    path('<int:sim_id>/complete/', views.complete_simulation, name='sim-complete'),
    path('experiments/', views.ExperimentListView.as_view(), name='experiment-list'),
    path('experiments/<int:pk>/', views.ExperimentDetailView.as_view(), name='experiment-detail'),
    path('experiments/<int:exp_id>/submit/', views.submit_experiment, name='experiment-submit'),
]
