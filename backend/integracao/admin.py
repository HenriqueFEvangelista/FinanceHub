from django.contrib import admin
from .models import HistoricoPesquisa


@admin.register(HistoricoPesquisa)
class HistoricoPesquisaAdmin(admin.ModelAdmin):
    list_display = ("simbolo", "data_pregao", "abertura", "maxima", "minima",
                    "fechamento", "volume", "data_pesquisa")
    search_fields = ("simbolo",)
    list_filter = ("data_pregao", "data_pesquisa")
    readonly_fields = ("data_pesquisa",)
