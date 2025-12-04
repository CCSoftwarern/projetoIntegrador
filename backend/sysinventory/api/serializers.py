from rest_framework import serializers
from django.contrib.auth.models import User
from sysinventory.models import (
    Setor,
    Funcionario,
    Equipamento,
    StatusEquipamento,
    Manutencao,
    Software,
    LicencaSoftware,
    LicencaPorEquipamento,
    HistoricoUsoEquipamento,
    Empresa
)

# -------------------------
# SETOR
# -------------------------
class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = '__all__'


# -------------------------
# FUNCIONÁRIO
# -------------------------
class FuncionarioSerializer(serializers.ModelSerializer):
    setor = SetorSerializer(read_only=True)
    setor_id = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(),
        source='setor',
        write_only=True
    )

    class Meta:
        model = Funcionario
        fields = [
            'id', 'nome', 'cpf', 'email', 'telefone',
            'setor', 'setor_id',
            'criado_por', 'data_cadastro'
        ]
        read_only_fields = ('criado_por', 'data_cadastro')


# -------------------------
# STATUS DO EQUIPAMENTO
# -------------------------
class StatusEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusEquipamento
        fields = '__all__'


# -------------------------
# EQUIPAMENTO
# -------------------------
class EquipamentoSerializer(serializers.ModelSerializer):
    funcionario = FuncionarioSerializer(read_only=True)
    funcionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.all(),
        source='funcionario',
        write_only=True
    )

    setor = SetorSerializer(read_only=True)
    setor_id = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(),
        source='setor',
        write_only=True
    )

    status = StatusEquipamentoSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=StatusEquipamento.objects.all(),
        source='status',
        write_only=True
    )

    class Meta:
        model = Equipamento
        fields = [
            'id', 'tipo', 'modelo', 'marca', 'numero_serie',
            'descricao', 'patrimonio',
            'data_aquisicao', 'data_cadastro',
            'funcionario', 'funcionario_id',
            'setor', 'setor_id',
            'status', 'status_id'
        ]


# -------------------------
# MANUTENÇÕES
# -------------------------
class ManutencaoSerializer(serializers.ModelSerializer):
    equipamento = EquipamentoSerializer(read_only=True)
    equipamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipamento.objects.all(),
        source='equipamento',
        write_only=True
    )

    class Meta:
        model = Manutencao
        fields = [
            'id', 'equipamento', 'equipamento_id',
            'tipo', 'descricao', 'data_manutencao',
            'custo', 'tecnico_responsavel',
            'registrado_por', 'data_registro'
        ]
        read_only_fields = ('registrado_por', 'data_registro')


# -------------------------
# SOFTWARE
# -------------------------
class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = '__all__'


# -------------------------
# LICENÇA DE SOFTWARE
# -------------------------
class LicencaSoftwareSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(),
        source='software',
        write_only=True
    )

    class Meta:
        model = LicencaSoftware
        fields = [
            'id', 'software', 'software_id',
            'chave', 'tipo_licenca',
            'quantidade_permitida', 'quantidade_usada',
            'data_aquisicao', 'data_expiracao',
            'fornecedor', 'observacao',
            'criado_por', 'data_cadastro'
        ]
        read_only_fields = ('criado_por', 'data_cadastro')


# -------------------------
# LICENÇAS POR EQUIPAMENTO
# -------------------------
class LicencaPorEquipamentoSerializer(serializers.ModelSerializer):
    licenca = LicencaSoftwareSerializer(read_only=True)
    licenca_id = serializers.PrimaryKeyRelatedField(
        queryset=LicencaSoftware.objects.all(),
        source='licenca',
        write_only=True
    )

    equipamento = EquipamentoSerializer(read_only=True)
    equipamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipamento.objects.all(),
        source='equipamento',
        write_only=True
    )

    class Meta:
        model = LicencaPorEquipamento
        fields = [
            'id',
            'licenca', 'licenca_id',
            'equipamento', 'equipamento_id',
            'data_instalacao'
        ]


# -------------------------
# HISTÓRICO DE USO DO EQUIPAMENTO
# -------------------------
class HistoricoUsoEquipamentoSerializer(serializers.ModelSerializer):
    equipamento = EquipamentoSerializer(read_only=True)
    equipamento_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipamento.objects.all(),
        source='equipamento',
        write_only=True
    )

    funcionario = FuncionarioSerializer(read_only=True)
    funcionario_id = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.all(),
        source='funcionario',
        write_only=True
    )

    setor = SetorSerializer(read_only=True)
    setor_id = serializers.PrimaryKeyRelatedField(
        queryset=Setor.objects.all(),
        source='setor',
        write_only=True
    )

    class Meta:
        model = HistoricoUsoEquipamento
        fields = [
            'id',
            'equipamento', 'equipamento_id',
            'funcionario', 'funcionario_id',
            'setor', 'setor_id',
            'data_inicio', 'data_fim',
            'observacao',
            'registrado_por', 'data_registro'
        ]
        read_only_fields = ('registrado_por', 'data_registro')

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'
        read_only_fields = ('data_cadastro',)

    def validate_cnpj(self, value):
        """
        Limpa o CNPJ removendo pontos, barras e traços e valida o tamanho (14 dígitos).
        Retorna o CNPJ somente com dígitos para armazenamento consistente.
        """
        if value is None:
            return value

        # Remove tudo que não for dígito
        import re
        digits = re.sub(r'\D', '', str(value))

        if len(digits) != 14:
            raise serializers.ValidationError("CNPJ inválido: deve conter 14 dígitos.")

        return digits
    
    class HistoricoUsoSerializer(serializers.ModelSerializer):
        class Meta:
            model = HistoricoUsoEquipamento
            fields = '__all__'
            read_only_fields = ('id',)

    def validate(self, data):
        """
        Validações gerais para garantir integridade das datas.
        """
        data_inicio = data.get('data_inicio')
        data_fim = data.get('data_fim')

        # Se houver data_fim, ela não pode ser anterior à data_inicio
        if data_inicio and data_fim and data_fim < data_inicio:
            raise serializers.ValidationError({
                "data_fim": "A data de término não pode ser anterior à data de início."
            })

        return data
    
class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = '__all__'
        read_only_fields = ('data_cadastro',)
    