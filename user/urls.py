from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.UserViewSet)
urlpatterns = router.urls
