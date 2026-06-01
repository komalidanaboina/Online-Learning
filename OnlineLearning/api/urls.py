from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import StudentViewSet


# DefaultRouter creates RESTful routes for the StudentViewSet automatically.
router = DefaultRouter()
router.register('students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]
