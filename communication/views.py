from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import LikeDislike
from .serializers import ActivitySerializer, LikeDislikeSerializer


class LikeDislikeAPIView(generics.CreateAPIView):
    """Add like/dislike to database"""

    serializer_class = LikeDislikeSerializer
    queryset = LikeDislike.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        """Pass request to serializer"""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class ActivityStatistic(generics.ListAPIView):
    """Likes statistic api"""

    serializer_class = ActivitySerializer
    queryset = LikeDislike.objects.all()

    def list(self, request, *args, **kwargs):
        """Likes analytic aggregated by day"""
        start_date = self.request.query_params.get("date_from", None)
        end_date = self.request.query_params.get("date_to", None)
        queryset = self.get_queryset().filter(
            created_at__range=(start_date, end_date)
        )
        queryset = (
            queryset.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(likes_count=Count("id"))
            .order_by("-date")
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
