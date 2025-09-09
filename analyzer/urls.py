from rest_framework_nested import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register(f'analyze', views.AnalyzeContentViewSet,
                basename='analyze-message')

urlpatterns = [
] + router.urls