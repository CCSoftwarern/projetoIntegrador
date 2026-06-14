
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from sysinventory.api import viewsets as sysinventory_viewsets
from sysinventory.views import dashboard_summary, home_page, login_api
route = routers.DefaultRouter()

route.register(r'empresas', sysinventory_viewsets.EmpresaViewSet)
route.register(r'funcionarios', sysinventory_viewsets.FuncionarioViewSet)
route.register(r'equipamentos', sysinventory_viewsets.EquipamentoViewSet)
route.register(r'manutencoes', sysinventory_viewsets.ManutencaoViewSet)
route.register(r'licencas-software', sysinventory_viewsets.LicencaSoftwareViewSet)
route.register(r'historico-uso', sysinventory_viewsets.HistoricoUsoViewSet)
route.register(r'setores', sysinventory_viewsets.SetorViewSet)
route.register(r'status-equipamento', sysinventory_viewsets.StatusEquipamentoViewSet)
route.register(r'softwares', sysinventory_viewsets.SoftwareViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login/', login_api, name='api_login'),
    path('api/v1/dashboard-summary/', dashboard_summary, name='dashboard_summary'),
    path('api/v1/', include(route.urls)),
    path('', home_page, name='home'),
]