from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('teams/', views.TeamListCreateView.as_view(), name='team-list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='team-detail'),
]
