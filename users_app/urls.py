from django.urls import path
from users_app import views

urlpatterns = [
    path('users/<int:user_id>/', views.UsersView.as_view()),
]
