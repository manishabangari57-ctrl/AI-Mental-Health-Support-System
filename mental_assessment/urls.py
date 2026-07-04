from django.urls import path
from . import views
from .views import assessment_view, assessment_history

urlpatterns = [
    path('', assessment_view, name="assessment"),
    path('history/', views.assessment_history, name="assessment_history"),
]