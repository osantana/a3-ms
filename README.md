# Vapor

Plataforma de distribuição digital de jogos (Projeto de Modelagem de Software A3).

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)

## Início Rápido

```bash
make up
```

Esse comando:

1. Inicia um banco de dados PostgreSQL 17
2. Compila e inicia a aplicação web
3. Executa as migrações do banco na inicialização
4. Carrega dados de demonstração automaticamente (usuários, jogos, pedidos)

A aplicação estará disponível em **http://localhost:8000**.

## Contas de Demonstração

| E-mail             | Senha      | Perfil        | Observações                          |
|--------------------|------------|---------------|--------------------------------------|
| admin@vapor.gg     | admin123   | Administrador | Pode aprovar/rejeitar jogos          |
| alice@vapor.gg     | alice123   | Usuário       | Publicou 4 jogos                     |
| bob@vapor.gg       | bob123     | Usuário       | Publicou 3 jogos                     |
| carlos@vapor.gg    | carlos123  | Usuário       | 4 jogos na biblioteca                |
| diana@vapor.gg     | diana123   | Usuário       | 3 jogos na biblioteca, 2 no carrinho |

## Parar a Aplicação

```bash
make down
```

Para remover também o volume do banco de dados (apagar todos os dados):

```bash
docker compose down -v
```

## Desenvolvimento Local (sem Docker)

Requer Python 3.13+, [uv](https://docs.astral.sh/uv/) e uma instância PostgreSQL em execução.

```bash
# Instalar dependências
uv sync

# Configurar a conexão com o banco (ajuste conforme necessário)
export DATABASE_URL=postgresql://vapor:vapor@localhost:5432/vapor

# Iniciar o servidor com auto-reload
make runserver
```

## Comandos do Makefile

| Comando          | Descrição                                          |
|------------------|----------------------------------------------------|
| `make up`        | Compilar e iniciar a aplicação com Docker Compose  |
| `make down`      | Parar e remover os containers                      |
| `make runserver` | Iniciar o servidor local (requer PostgreSQL)       |
| `make lint`      | Executar verificações do ruff (linter e formatação) |
| `make format`    | Formatar o código automaticamente com ruff         |
| `make all`       | Gerar o documento PDF do projeto                   |
| `make clean`     | Remover o PDF gerado                               |
