from django.contrib import admin
from django.urls import path
from integracao.views import buscar_acao

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/acoes/<str:simbolo>/", buscar_acao, name="buscar_acao"),
]
