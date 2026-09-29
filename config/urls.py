"""Root URL configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portfolio.urls")),
]

# Serve uploaded images/files while developing.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Portfolio admin"
admin.site.site_title = "Portfolio admin"
admin.site.index_title = "Manage your site content"
