from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="HistoricoPesquisa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("simbolo", models.CharField(db_index=True, max_length=20)),
                ("data_pregao", models.DateField()),
                ("abertura", models.DecimalField(decimal_places=4, max_digits=20)),
                ("maxima", models.DecimalField(decimal_places=4, max_digits=20)),
                ("minima", models.DecimalField(decimal_places=4, max_digits=20)),
                ("fechamento", models.DecimalField(decimal_places=4, max_digits=20)),
                ("volume", models.PositiveBigIntegerField()),
                ("data_pesquisa", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Histórico de pesquisa",
                "verbose_name_plural": "Histórico de pesquisas",
                "ordering": ["-data_pesquisa", "-pk"],
            },
        ),
    ]
