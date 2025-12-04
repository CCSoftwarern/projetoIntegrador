from rest_framework import viewsets
from sysinventory.models import Empresa, Funcionario, Equipamento, Manutencao, LicencaSoftware, HistoricoUsoEquipamento, Setor, StatusEquipamento, Software
from .serializers import (
    EmpresaSerializer, FuncionarioSerializer, EquipamentoSerializer,
    ManutencaoSerializer, LicencaSoftwareSerializer, HistoricoUsoEquipamentoSerializer, SetorSerializer, StatusEquipamentoSerializer, SoftwareSerializer
)

# ------------------------------
# Empresa
# ------------------------------
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


# ------------------------------
# Funcionário
# ------------------------------
class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer


# ------------------------------
# Equipamento
# ------------------------------
class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer


# ------------------------------
# Manutenção
# ------------------------------
class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer


# ------------------------------
# Licenças de Software
# ------------------------------
class LicencaSoftwareViewSet(viewsets.ModelViewSet):
    queryset = LicencaSoftware.objects.all()
    serializer_class = LicencaSoftwareSerializer


# ------------------------------
# Histórico de Uso de Equipamento
# ------------------------------
class HistoricoUsoViewSet(viewsets.ModelViewSet):
    queryset = HistoricoUsoEquipamento.objects.all()
    serializer_class = HistoricoUsoEquipamentoSerializer


# ------------------------------
# Setores
# ------------------------------

class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer

# ------------------------------
# Status do Equipamento
# ------------------------------

class StatusEquipamentoViewSet(viewsets.ModelViewSet):
    queryset = StatusEquipamento.objects.all()
    serializer_class = StatusEquipamentoSerializer


# ------------------------------
#  Sofware
# ------------------------------
class SoftwareViewSet(viewsets.ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer