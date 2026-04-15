# Catálogo de Produtos — API REST com Django + AWS Elastic Beanstalk

> **AP1 — Disciplina BDCC_26.1_8001**
> Deploy em produção: [http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/api/](http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/api/)

---

## Descrição

Este projeto foi desenvolvido como entrega da AP1 da disciplina de Cloud Computing. O objetivo é demonstrar a construção de uma API RESTful utilizando Django REST Framework, com modelagem de dados relacional, e o deploy da aplicação na AWS utilizando o serviço Elastic Beanstalk.

A API gerencia um catálogo de produtos categorizados, expondo endpoints para criação, leitura, atualização e remoção de **Categorias** e **Produtos**, com relacionamento entre as duas entidades via chave estrangeira.

---

## Funcionalidades

- Cadastro, listagem, edição e remoção de Categorias
- Cadastro, listagem, edição e remoção de Produtos
- Relacionamento entre Produto e Categoria via ForeignKey
- Campo `categoria_nome` exposto no retorno de Produtos para facilitar leitura
- Interface administrativa via Django Admin (`/admin/`)
- Healthcheck na raiz da aplicação (`/`)
- Deploy automatizado na AWS Elastic Beanstalk com migrations e coleta de arquivos estáticos

---

## Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.12 | Linguagem principal |
| Django | 6.0.4 | Framework web |
| Django REST Framework | 3.17.1 | Construção da API REST |
| Gunicorn | 25.3.0 | Servidor WSGI para produção |
| SQLite | — | Banco de dados (ambiente local) |
| AWS Elastic Beanstalk | — | Plataforma de deploy |
| AWS EC2 | — | Infraestrutura de servidor (provisionada pelo EB) |

---

## Modelagem de Dados

### Categoria

Entidade criada nesta AP1. Representa a classificação de um produto.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária (auto) |
| `nome` | CharField(100) | Nome da categoria |
| `descricao` | TextField | Descrição opcional da categoria |

### Produto

Entidade principal do projeto. Representa um item do catálogo.

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | Integer | Chave primária (auto) |
| `nome` | CharField(200) | Nome do produto |
| `descricao` | TextField | Descrição opcional |
| `preco` | DecimalField | Preço com até 2 casas decimais |
| `estoque` | IntegerField | Quantidade em estoque |
| `categoria` | ForeignKey | Referência para Categoria |

### Relacionamento

`Produto` possui uma `ForeignKey` para `Categoria` com `on_delete=SET_NULL`, o que significa que ao remover uma categoria, os produtos associados não são excluídos — o campo `categoria` é simplesmente anulado. Esse comportamento preserva a integridade dos produtos mesmo em caso de reorganização das categorias.

---

## Endpoints da API

Base URL local: `http://127.0.0.1:8000`
Base URL produção: `http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com`

### Healthcheck

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Retorna `{"status": "ok"}` |

### Categorias

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/categorias/` | Lista todas as categorias |
| POST | `/api/categorias/` | Cria uma nova categoria |
| GET | `/api/categorias/{id}/` | Detalhe de uma categoria |
| PUT | `/api/categorias/{id}/` | Atualização completa |
| PATCH | `/api/categorias/{id}/` | Atualização parcial |
| DELETE | `/api/categorias/{id}/` | Remove a categoria |

### Produtos

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/produtos/` | Lista todos os produtos |
| POST | `/api/produtos/` | Cria um novo produto |
| GET | `/api/produtos/{id}/` | Detalhe de um produto |
| PUT | `/api/produtos/{id}/` | Atualização completa |
| PATCH | `/api/produtos/{id}/` | Atualização parcial |
| DELETE | `/api/produtos/{id}/` | Remove o produto |

### Exemplos de payload

**POST `/api/categorias/`**
```json
{
  "nome": "Eletrônicos",
  "descricao": "Computadores, celulares e acessórios"
}
```

**POST `/api/produtos/`**
```json
{
  "nome": "Notebook Dell Inspiron",
  "descricao": "15 polegadas, 16GB RAM, SSD 512GB",
  "preco": "3499.90",
  "estoque": 10,
  "categoria": 1
}
```

**Resposta de GET `/api/produtos/`**
```json
[
  {
    "id": 1,
    "nome": "Notebook Dell Inspiron",
    "descricao": "15 polegadas, 16GB RAM, SSD 512GB",
    "preco": "3499.90",
    "estoque": 10,
    "categoria": 1,
    "categoria_nome": "Eletrônicos"
  }
]
```

---

## Como Rodar Localmente

### Pré-requisitos

- Python 3.12 ou superior instalado
- pip disponível no terminal

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Aplicar as migrations

```bash
python manage.py migrate
```

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://127.0.0.1:8000`.

---

## Criar Usuário Administrador

Para acessar o painel em `/admin/`, crie um superusuário:

```bash
python manage.py createsuperuser
```

Preencha os campos solicitados (username, e-mail opcional, senha). Em seguida acesse `http://127.0.0.1:8000/admin/` com as credenciais criadas.

---

## Estrutura do Projeto

```
.
├── .ebextensions/
│   └── django.config        # Configuração do Elastic Beanstalk
├── catalogo/
│   ├── settings.py          # Configurações do projeto
│   ├── urls.py              # Rotas principais
│   └── wsgi.py              # Ponto de entrada WSGI
├── produtos/
│   ├── admin.py             # Registro no Django Admin
│   ├── models.py            # Modelos Categoria e Produto
│   ├── serializers.py       # Serializers DRF
│   ├── views.py             # ViewSets da API
│   ├── urls.py              # Rotas da app
│   └── migrations/          # Histórico de migrations
├── manage.py
├── Procfile                 # Comando de inicialização (Elastic Beanstalk)
└── requirements.txt         # Dependências do projeto
```

---

## Deploy na AWS Elastic Beanstalk

O deploy foi realizado seguindo o fluxo abaixo:

1. **Empacotamento:** os arquivos do projeto (sem `.venv/`, `db.sqlite3` e `__pycache__/`) foram compactados em `app.zip`
2. **Criação da Application:** no console da AWS, foi criada uma nova Application no serviço Elastic Beanstalk
3. **Configuração do Environment:** plataforma Python 3.12, região us-east-1, modalidade Single Instance (free tier)
4. **Upload do ZIP:** o arquivo `app.zip` foi enviado diretamente pelo console
5. **Automação via `.ebextensions`:** ao subir, o ambiente executa automaticamente:
   - `python manage.py migrate --noinput`
   - `python manage.py collectstatic --noinput`
   - Criação do superusuário admin
6. **Variáveis de ambiente** configuradas no painel do EB: `DJANGO_DEBUG=False`, `DJANGO_SETTINGS_MODULE`, `DJANGO_ALLOWED_HOSTS`

---

## API em Produção

> **A API está no ar e acessível pelo link abaixo:**

**[http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/api/](http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/api/)**

| Endpoint | Link direto |
|---|---|
| Raiz da API | [/api/](http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/api/) |
| Categorias | [/api/categorias/](http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/api/categorias/) |
| Produtos | [/api/produtos/](http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/api/produtos/) |
| Admin | [/admin/](http://catalogo-produtos-env.eba-5rj9dgp4.us-east-1.elasticbeanstalk.com/admin/) |
