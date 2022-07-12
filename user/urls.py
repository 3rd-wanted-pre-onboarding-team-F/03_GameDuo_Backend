from django.urls import path 
from django.conf.urls import include
from user import views


urlpatterns = [
    path('', views.account_list),
    path('<int:pk>/', views.account),
    path('login/', views.login),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
