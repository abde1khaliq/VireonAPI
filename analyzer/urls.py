from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(f'analyze', views.AnalyzeContentViewSet,
                basename='analyze-message')

urlpatterns = [
] + router.urls