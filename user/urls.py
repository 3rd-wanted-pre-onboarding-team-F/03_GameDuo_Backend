from django.urls import path 
from .views import RegisterView, LoginView, TotalScoreView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('<int:pk>/', TotalScoreView.as_view()),
    path('login/', LoginView.as_view()),
]
