from django.urls import path

from .views import RegistrationAPIView, UserActivityAPIView


app_name = "accounts"

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="sign_up"),
    path(
        "user-activity/<int:pk>/",
        UserActivityAPIView.as_view(),
        name="user_activity",
    ),
]
