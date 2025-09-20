from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register(f'analyze', AnalyzeContentViewSet,
                basename='analyze-message')

urlpatterns = [
] + router.urls