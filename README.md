# SysInventory

## Descrição do Projeto
"Trata-se de um sistema com finalidade acadêmica, desenvolvido para o inventário de ativos de informática, atendendo aos requisitos da disciplina de Projeto Integrador do IFRN – Campus Parnamirim/RN."

# 🚀 Projeto Django + PostgreSQL com Docker

## 📋 Pré-requisitos
- Docker instalado
- Docker Compose instalado
- Git instalado

---

## 📦 Clonar o repositório

```bash
git clone https://github.com/CCSoftwarern/projetoIntegrador.git

```
## Passo a Passo

- No terminal: cd projetoIntegrador
- No terminal: cd backend
- No terminal: code .
- Vai abrir um novo VSCODE, feche o antigo pra não se confundir.
- Abra o terminal e ponha: docker-compose up --build
- Abra um novo terminal para criar as tabelas: docker-compose exec web python manage.py migrate
- No terminal pra criar superusuario: docker-compose exec web python manage.py createsuperuser
- Crie o usuario: suporte
- Ponha seu e-mail: seuemail@email.com 
- Ponha qualuer senha:123master




