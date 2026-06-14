from django.contrib.auth import get_user_model
from django.test import TestCase

from sysinventory.models import Empresa, Funcionario, Setor, StatusEquipamento


class LoginApiTests(TestCase):
    def test_login_endpoint_accepts_json_credentials_without_csrf_token(self):
        User = get_user_model()
        User.objects.create_user(username='suporte', password='123master')

        response = self.client.post(
            '/api/v1/login/',
            {'username': 'suporte', 'password': '123master'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())
        self.assertEqual(response.json()['user']['username'], 'suporte')


class DashboardSummaryApiTests(TestCase):
    def test_dashboard_summary_returns_all_requested_collections(self):
        empresa = Empresa.objects.create(cnpj='12345678000199', razao_social='Empresa Teste')
        setor = Setor.objects.create(nome='TI')
        status = StatusEquipamento.objects.create(status='Em uso')
        Funcionario.objects.create(
            nome='Maria',
            cpf='12345678901',
            email='maria@example.com',
            telefone='11999999999',
            setor=setor,
        )

        response = self.client.get('/api/v1/dashboard-summary/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['empresas'][0]['id'], empresa.id)
        self.assertEqual(response.json()['funcionarios'][0]['nome'], 'Maria')
        self.assertEqual(response.json()['setores'][0]['nome'], 'TI')
        self.assertEqual(response.json()['status_equipamento'][0]['status'], 'Em uso')
