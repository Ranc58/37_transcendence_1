from django.urls import path
from users_app import views

urlpatterns = [
    path('<int:pk>/', views.UsersView.as_view(), name='user_detail'),
]
