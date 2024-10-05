from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import SubmitDataView

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Description of your API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path('swagger/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('openapi-schema/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('submit/', SubmitDataView.as_view(), name='submit'),
]
