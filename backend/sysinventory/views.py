from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sysinventory.api.serializers import (
    EmpresaSerializer,
    FuncionarioSerializer,
    SetorSerializer,
    StatusEquipamentoSerializer,
)
from sysinventory.models import Empresa, Funcionario, Setor, StatusEquipamento


def home_page(request):
    return render(request, "home.html")


@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_summary(request):
    """Retorna empresas, funcionários, setores e status de equipamento em um único endpoint."""
    return Response({
        'empresas': EmpresaSerializer(Empresa.objects.all(), many=True).data,
        'funcionarios': FuncionarioSerializer(Funcionario.objects.all(), many=True).data,
        'setores': SetorSerializer(Setor.objects.all(), many=True).data,
        'status_equipamento': StatusEquipamentoSerializer(
            StatusEquipamento.objects.all(),
            many=True,
        ).data,
    }, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response(
            {'detail': 'Credenciais inválidas.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        'token': token.key,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
    }, status=status.HTTP_200_OK)