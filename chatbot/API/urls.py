from django.urls import path
from .views import gpt4_risk_assessment, index

urlpatterns = [
    path('api/risk_assessment/', gpt4_risk_assessment, name='gpt4_risk_assessment'),
    path('', index, name='index'),
]

