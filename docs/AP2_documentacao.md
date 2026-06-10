# AP2 - Documentacao de Deploy e Arquitetura

## Resumo

Este projeto evolui a API da AP1 para uma arquitetura de nuvem com:

- Elastic Beanstalk executando a aplicacao Django REST.
- RDS MySQL como banco relacional de producao.
- Amazon S3 como armazenamento de midia dos produtos.
- Modelos novos para um fluxo simples de e-commerce: `Pedido` e `PedidoItem`.

## URL de Producao

- Base URL: `http://catalogo-ap2-env.eba-e2j4yxvh.us-east-1.elasticbeanstalk.com`
- API root: `http://catalogo-ap2-env.eba-e2j4yxvh.us-east-1.elasticbeanstalk.com/api/`
- Admin: `http://catalogo-ap2-env.eba-e2j4yxvh.us-east-1.elasticbeanstalk.com/admin/`

## Recursos AWS

| Recurso | Valor |
|---|---|
| Elastic Beanstalk Application | `catalogo-ap2` |
| Elastic Beanstalk Environment | `Catalogo-ap2-env` |
| Plataforma | Python 3.12 on Amazon Linux 2023 |
| Versao implantada | `catalogo-ap2-version-4` |
| RDS | `ap2-db.core80gmoru4.us-east-1.rds.amazonaws.com` |
| Banco | `ap2db` |
| S3 Bucket | `ap2-media-augusto` |
| Regiao | `us-east-1` |

## Variaveis de Ambiente

Configuradas no Elastic Beanstalk:

| Variavel | Finalidade |
|---|---|
| `DJANGO_SECRET_KEY` | Chave secreta do Django em producao |
| `DJANGO_SETTINGS_MODULE` | Define `catalogo.settings` |
| `DJANGO_DEBUG` | Mantem debug desligado em producao |
| `DJANGO_ALLOWED_HOSTS` | Libera o dominio do Elastic Beanstalk |
| `DB_HOST` | Endpoint do RDS MySQL |
| `DB_NAME` | Nome do banco no RDS |
| `DB_USER` | Usuario do banco |
| `DB_PASSWORD` | Senha do banco |
| `AWS_STORAGE_BUCKET_NAME` | Bucket S3 para midia |
| `AWS_S3_REGION_NAME` | Regiao do bucket S3 |
| `DJANGO_ADMIN_PASSWORD` | Senha do admin criado no deploy, se configurada |

## Decisoes Tecnicas

- O projeto usa SQLite localmente quando `DB_HOST` nao esta definido.
- O projeto usa RDS MySQL em producao quando `DB_HOST` esta definido.
- O projeto usa armazenamento local de midia quando `AWS_STORAGE_BUCKET_NAME` nao esta definido.
- O projeto usa S3 em producao quando `AWS_STORAGE_BUCKET_NAME` esta definido.
- O driver MySQL de producao e `mysqlclient==2.2.7`, necessario para compatibilidade com Django 6.
- O `.ebextensions/django.config` instala pacotes nativos para compilar o `mysqlclient` no Amazon Linux 2023.
- O deploy executa `migrate`, `collectstatic` e criacao de superusuario via `container_commands`.
- O usuario administrador de producao e criado automaticamente com username `admin`; a senha deve vir de `DJANGO_ADMIN_PASSWORD`.

## Modelos Adicionados na AP2

### Produto

O modelo `Produto` recebeu o campo:

- `imagem`: `ImageField`, usado para upload de imagem do produto.

### Pedido

Campos principais:

- `status`
- `criado_em`
- `atualizado_em`
- `total`

### PedidoItem

Campos principais:

- `pedido`
- `produto`
- `quantidade`
- `preco_unitario`
- `subtotal`

## Endpoints Validados

Validacao realizada em 10/06/2026:

| Endpoint | Resultado |
|---|---|
| `GET /` | HTTP 200, `{"status": "ok"}` |
| `GET /api/` | HTTP 200 |
| `GET /api/categorias/` | HTTP 200, lista retornada |
| `GET /api/produtos/` | HTTP 200, lista retornada |
| `GET /api/pedidos/` | HTTP 200, lista retornada |
| `GET /api/pedido-itens/` | HTTP 200, lista retornada |
| `GET /admin/` | HTTP 200, tela de login aberta |
| Login `/admin/` | Sucesso com usuario administrador `admin` |
| `POST /api/categorias/` | HTTP 201, categoria criada |
| `PATCH /api/categorias/{id}/` | HTTP 200, categoria atualizada |
| `DELETE /api/categorias/{id}/` | HTTP 204, categoria temporaria removida |
| `POST /api/produtos/` com imagem | HTTP 201, produto criado e imagem salva no S3 |
| `POST /api/pedidos/` | HTTP 201, pedido criado |
| `POST /api/pedido-itens/` | HTTP 201, item de pedido criado |

## Evidencias Funcionais

- Produto criado em producao: `id=1`.
- URL da imagem persistida no S3: `https://ap2-media-augusto.s3.amazonaws.com/produtos/ap2-validacao-produto.png`.
- Download direto da imagem no S3 validado com HTTP 200, `Content-Type: image/png`.
- Pedido criado em producao: `id=2`.
- Item de pedido criado em producao: `id=1`, subtotal `39.80`.
- Login no Django Admin validado com usuario administrador.

## Dificuldades e Solucoes

| Dificuldade | Solucao |
|---|---|
| Deploy falhando no `01_migrate` | Troca de `PyMySQL` por `mysqlclient==2.2.7`, compativel com Django 6 |
| Dependencias nativas do MySQL no Elastic Beanstalk | Inclusao de `gcc`, `python3-devel`, `mariadb105-devel` e `pkgconf-pkg-config` em `.ebextensions/django.config` |
| Uso de credenciais AWS em ambiente com restricoes de IAM | Configuracao para permitir uso do EC2 Instance Role pelo `boto3` |
| Separar dev e prod | SQLite e media local em desenvolvimento; RDS e S3 quando variaveis de ambiente existem |

## Evidencias Manuais Ainda Recomendadas

- Print do ambiente Elastic Beanstalk com Health Ok.
- Print do RDS mostrando a instancia `ap2-db` e/ou conexoes ativas.
- Print do bucket S3 mostrando o arquivo `produtos/ap2-validacao-produto.png`.
- Print do Django Admin logado.
- Print de um pedido ou item de pedido criado pela API/Admin.

## Resultado Atual

O ambiente Elastic Beanstalk esta com Health Ok, o deploy da versao `catalogo-ap2-version-4` foi concluido, e os endpoints publicos da API, o login admin, o upload para S3 e o fluxo basico de pedido foram validados.
