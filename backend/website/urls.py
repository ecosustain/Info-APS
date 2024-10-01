# Em website/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from website.views.apihub_views import ApiHubView
from website.views.automacao import AutomacaoView
from website.views.database_views import DatabaseView
from website.views.er_model_views import ErModelView
from website.views.index_views import IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("database/", DatabaseView.as_view(), name="database"),
    path("er_model/", ErModelView.as_view(), name="er_model"),
    path("automacao/", AutomacaoView.as_view(), name="automacao"),
    path("apihub/", ApiHubView.as_view(), name="apihub"),
]

# Adiciona estas linhas para servir arquivos estáticos e de mídia no ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
