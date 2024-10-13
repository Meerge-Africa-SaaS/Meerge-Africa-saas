from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from rest_framework.schemas import get_schema_view

from config import api
from restaurants import views as restaurant_views
from search import views as search_views

urlpatterns = [
    path("meerge/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    path("", include("home.urls")),
    path("api/", include("core.urls")),
    path(
        "shema_api/", 
        get_schema_view(title="API Schema", 
                        description="The api endpoints in the second drf link sent earlier has been converted to swagger for better use.",
                        version="1.0.0"), 
        name="schema_api"
        ),
    path(
        "swagger-ui",
        TemplateView.as_view(
            template_name="api_docs.html",
            extra_context={
                'schema_url': 'schema_api'
            },
        ),
        name="swagger-ui"
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
    #path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
