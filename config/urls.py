from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("devices", FCMDeviceAuthorizedViewSet)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("auth/", include("agriwise.users.urls")),
    path("profiles/", include("agriwise.users.api.urls")),
    path("crop_recommendation/", include("agriwise.crop_recomendation.urls")),
    path("soil-fertilizer/", include("agriwise.soil_fertilizer.urls")),
    path("soil-quality/", include("agriwise.soil_quality.urls")),
    path("soil-type/", include("agriwise.soil_type.urls")),
    path("profile-upgrade/", include("agriwise.agriculture_specialist.urls")),
    path(
        "custom-admin/profile-upgrade/",
        include("agriwise.agriculture_specialist.admin_urls"),
    ),
    path("chat-api/", include("agriwise.chat.urls")),
    path("firebase-api/", include(router.urls)),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
