from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField(verbose_name="nome", max_length=128)
    price = models.FloatField(verbose_name="preco")
    photo = models.ImageField(verbose_name="foto")

    def __str__(self):
        return f"{self.name} - R${self.price:.2f}"

    class Meta:
        verbose_name = "Produto"


class Client(models.Model):

    cpf = models.CharField(verbose_name="cpf", max_length=128)
    street = models.CharField(verbose_name="rua", max_length=255)
    district = models.CharField(verbose_name="bairro", max_length=255)
    number = models.CharField(verbose_name="número", max_length=128, default="S/N")
    city = models.CharField(verbose_name="cidade", max_length=128)
    complement = models.CharField(verbose_name="complemento", max_length=11,
                                  choices=(("casa", "Casa"), ("apartamento", "Apartamento")))
    reference_point = models.CharField(verbose_name="ponto de referência", max_length=255, blank=True, null=True)
    uf = models.CharField(verbose_name="UF", max_length=2)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,
                                related_name="client", editable=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Cliente"


class Service(models.Model):
    service = models.CharField(verbose_name="serviço", max_length=144)
    description = models.TextField(verbose_name="descrição", max_length=255)
    value = models.FloatField(verbose_name="valor")

    def __str__(self):
        return "%s %.2f" % (self.service, self.value)


class Schedule(models.Model):
    service = models.ForeignKey(verbose_name="serviço", to=Service, related_name="schedule", on_delete=models.PROTECT)
    client = models.ForeignKey(verbose_name="cliente", to=Client, related_name="client", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="data")
    accomplished = models.BooleanField(verbose_name="executado", default=False)
