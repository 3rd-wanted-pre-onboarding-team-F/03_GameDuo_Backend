from django.urls import path 
from django.conf.urls import include

from user import views


user_detail = views.TotalScoreAPI.as_view({
    'get': 'retrieve'
})


urlpatterns = [
    path('', views.account_list),
    path('<int:user_id>/', user_detail),
    path('login/', views.login),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
