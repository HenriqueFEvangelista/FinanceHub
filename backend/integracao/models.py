from django.db import models


class HistoricoPesquisa(models.Model):
    simbolo = models.CharField(max_length=20, db_index=True)
    data_pregao = models.DateField()
    abertura = models.DecimalField(max_digits=20, decimal_places=4)
    maxima = models.DecimalField(max_digits=20, decimal_places=4)
    minima = models.DecimalField(max_digits=20, decimal_places=4)
    fechamento = models.DecimalField(max_digits=20, decimal_places=4)
    volume = models.PositiveBigIntegerField()
    data_pesquisa = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Histórico de pesquisa"
        verbose_name_plural = "Histórico de pesquisas"
        ordering = ["-data_pesquisa", "-pk"]

    def __str__(self):
        return f"{self.simbolo} - {self.data_pregao}"
