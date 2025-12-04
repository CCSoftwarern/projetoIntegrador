from django.db import models
from django.contrib.auth.models import User  # caso use o Django Auth padrão

# Modelo para empresas
class Empresa(models.Model):
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=150, blank=True, null=True)
    bairro = models.CharField(max_length=150, blank=True, null=True)
    cidade = models.CharField(max_length=150, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = "empresa"
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"

# Modelo para setores dentro da empresa
class Setor(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        db_table = 'setor'

    def __str__(self):
        return self.nome

# Modelo para funcionários da empresa
class Funcionario(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True)

    # usuario do sistema que cadastrou o funcionário
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'funcionario'

    def __str__(self):
        return f"{self.nome} ({self.setor})"


class StatusEquipamento(models.Model):
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'status_equipamento'

    def __str__(self):
        return self.status


# Modelo para equipamentos
class Equipamento(models.Model):
    TIPO_CHOICES = [
        ('NOTEBOOK', 'Notebook'),
        ('DESKTOP', 'Desktop'),
        ('MONITOR', 'Monitor'),
        ('IMPRESSORA', 'Impressora'),
        ('CELULAR', 'Celular'),
        ('TABLET', 'Tablet'),
        ('ROTEADOR', 'Roteador'),
        ('SWITCH', 'Switch'),
        ('OUTRO', 'Outro'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    modelo = models.CharField(max_length=150)
    marca = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True, unique=True)

    # 🔥 Agora vinculado ao FUNCIONÁRIO (quem usa)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)

    # setor do equipamento (geralmente mesmo setor do funcionário)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True)

    status = models.ForeignKey(StatusEquipamento, on_delete=models.SET_NULL, null=True)

    descricao = models.TextField(blank=True, null=True)
    patrimonio = models.CharField(max_length=50, blank=True, null=True)

    data_aquisicao = models.DateField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'equipamento'

    def __str__(self):
        return f"{self.tipo} - {self.modelo} ({self.numero_serie})"

# Modelo para manutenções de equipamentos
class Manutencao(models.Model):
    TIPO_MANUTENCAO_CHOICES = [
        ('CORRETIVA', 'Manutenção Corretiva'),
        ('PREVENTIVA', 'Manutenção Preventiva'),
        ('ATUALIZACAO', 'Atualização de Software'),
        ('LIMPEZA', 'Limpeza Técnica'),
        ('OUTRO', 'Outro Tipo'),
    ]

    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name='manutencoes'
    )

    tipo = models.CharField(max_length=20, choices=TIPO_MANUTENCAO_CHOICES)

    descricao = models.TextField()
    data_manutencao = models.DateField()
    custo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    tecnico_responsavel = models.CharField(max_length=150, blank=True, null=True)

    # Usuário do sistema que registrou a manutenção
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "manutencao"
        verbose_name = "Manutenção"
        verbose_name_plural = "Manutenções"

    def __str__(self):
        return f"{self.tipo} - {self.equipamento.modelo} ({self.data_manutencao})"


class Software(models.Model):
    nome = models.CharField(max_length=150)
    fornecedor = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        db_table = 'software'

    def __str__(self):
        return self.nome

# Modelo para licenças de software
class LicencaSoftware(models.Model):
    TIPO_LICENCA_CHOICES = [
        ('OEM', 'OEM'),
        ('VOLUME', 'Volume Licensing'),
        ('SUBSCRIPTION', 'Assinatura'),
        ('LIFETIME', 'Vitalícia'),
        ('FREE', 'Gratuita'),
    ]

    software = models.ForeignKey(
        Software,
        on_delete=models.CASCADE,
        related_name='licencas'
    )

    chave = models.CharField(max_length=200, unique=True)
    tipo_licenca = models.CharField(max_length=20, choices=TIPO_LICENCA_CHOICES)

    quantidade_permitida = models.IntegerField(default=1)
    quantidade_usada = models.IntegerField(default=0)

    data_aquisicao = models.DateField(blank=True, null=True)
    data_expiracao = models.DateField(blank=True, null=True)

    fornecedor = models.CharField(max_length=150, blank=True, null=True)

    observacao = models.TextField(blank=True, null=True)

    # Usuário do sistema que cadastrou
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'licenca_software'
        verbose_name = 'Licença de Software'
        verbose_name_plural = 'Licenças de Software'

    def __str__(self):
        return f"{self.software.nome} - {self.chave}"

class LicencaPorEquipamento(models.Model):
    licenca = models.ForeignKey(
        LicencaSoftware,
        on_delete=models.CASCADE,
        related_name='instalacoes'
    )
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name='licencas'
    )

    data_instalacao = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'licenca_por_equipamento'
        unique_together = ('licenca', 'equipamento')

    def __str__(self):
        return f"{self.licenca.software.nome} em {self.equipamento.modelo}"

# Modelo para histórico de uso de equipamentos
class HistoricoUsoEquipamento(models.Model):
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.CASCADE,
        related_name='historico_uso'
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='historico_equipamentos'
    )

    setor = models.ForeignKey(
        Setor,
        on_delete=models.SET_NULL,
        null=True
    )

    data_inicio = models.DateField()
    data_fim = models.DateField(blank=True, null=True)  # fica vazio enquanto o funcionário ainda está usando

    observacao = models.TextField(blank=True, null=True)

    # Usuário do sistema que registrou
    registrado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'historico_uso_equipamento'
        verbose_name = 'Histórico de Uso'
        verbose_name_plural = 'Históricos de Uso'

    def __str__(self):
        return f"{self.equipamento.modelo} usado por {self.funcionario.nome}"
    

class Meta:
    db_table = 'setor'

def __str__(self):
    return self.nome


