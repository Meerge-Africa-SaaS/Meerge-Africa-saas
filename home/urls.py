from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("index/", TemplateView.as_view(template_name="index.html"), name="index"),
    # path('orders/', include('orders.urls')),
    # path('core/', include('core.urls')),
    # path('customers/', include('customers.urls')),
    # path('world/', include('world.urls')),
    # path('inventory/', include('inventory.urls')),
    # path('restaurants/', include('restaurants.urls')),
    path("htmx/", views.htmx_home, name="htmx"),
]
