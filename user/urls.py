from django.urls import path
from django.conf.urls import include
from .views import RegisterView, LoginView, TotalScoreAPI


user_detail = TotalScoreAPI.as_view({"get": "retrieve"})


urlpatterns = [
    path("<int:user_id>/", user_detail),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
]
