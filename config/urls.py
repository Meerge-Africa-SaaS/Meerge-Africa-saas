from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from rest_framework.schemas import get_schema_view

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config import api
from core.views import PasswordResetDoneView, PasswordResetView
from restaurants import views as restaurant_views
from search import views as search_views

urlpatterns = [
    path("meerge/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("", include("home.urls")),
    path("api/", include("core.urls")),
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/swagger/docs", SpectacularSwaggerView.as_view(url_name="schema")),
    
    path(
        "accounts/password/reset/",
        PasswordResetView.as_view(),
        name="account_reset_password",
    ),
    path(
        "accounts/password/reset/done/",
        PasswordResetDoneView.as_view(),
        name="account_reset_password_done",
    ),
    path("accounts/", include("allauth.urls")),
    path("", include(api)),
    path("accounts/", include("allauth.urls")),
    path("restaurant/", include("restaurants.urls")),
    path("customers/", include("customers.urls")),
    path("inventory/", include("inventory.urls")),
    path("orders/", include("orders.urls")),
    path(
        "<slug:custom_link>",
        restaurant_views.RestaurantDetailView.as_view(),
        name="restaurant_detail",
    ),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    path("pages/", include(wagtail_urls)),
]
