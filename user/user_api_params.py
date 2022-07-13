from drf_yasg import openapi

user_post_params = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "username": openapi.Schema(type=openapi.TYPE_STRING, description="username"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="passwd"),
    },
)