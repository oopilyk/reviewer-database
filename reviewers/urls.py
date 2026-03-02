from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewerViewSet

router = DefaultRouter()
router.register(r'reviewers', ReviewerViewSet, basename='reviewer')

urlpatterns = [
    path('', include(router.urls)),
]
