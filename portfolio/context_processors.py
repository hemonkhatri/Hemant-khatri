"""Template context shared by every page."""
from django.db import Error

from .models import Profile


def site_profile(request):
    """Expose the single Profile row to all templates as `profile`."""
    try:
        profile = Profile.objects.first()
    except Error:
        # The table doesn't exist yet (e.g. before the first migrate).
        profile = None
    return {"profile": profile}
