from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import PostListCreateAPIView,BlogView,BlogUpdate,BlogCreate,BlogDetail

urlpatterns = [
    path('', views.PostListCreateAPIView.as_view()),
    path('<str:post_id>/', views.PostRetrieveAPIView.as_view()),
    path('update/<str:post_id>/', views.PostUpdateAPIView.as_view()),
    path('delete/<str:post_id>/', views.PostDeleteAPIView.as_view()),

]