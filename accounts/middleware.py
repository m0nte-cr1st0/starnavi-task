from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class UpdateLastRequestMiddleware(MiddlewareMixin):
    """Last activity middleware"""

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Update user last_request"""
        assert hasattr(
            request, "user"
        ), "The UpdateLastRequestMiddleware requires authentication middleware to be installed."
        if request.user.is_authenticated:
            request.user.last_request = timezone.now()
            request.user.save(update_fields=("last_request",))
