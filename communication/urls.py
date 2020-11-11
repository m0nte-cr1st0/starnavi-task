from django.urls import path

from .views import ActivityStatistic, LikeDislikeAPIView


urlpatterns = [
    path("action/", LikeDislikeAPIView.as_view(), name="action_view"),
    path("activity/", ActivityStatistic.as_view(), name="action_view"),
]
