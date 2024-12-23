# Mock GitLab API

Uma API mock que simula endpoints selecionados do GitLab para fins de desenvolvimento e testes.

## 🚀 Visão Geral

Esta API fornece dados simulados para endpoints comuns do GitLab, incluindo projetos, merge requests e commits. É útil para desenvolvimento e testes quando você não quer depender da API real do GitLab.

### Principais Funcionalidades

- Geração automática de dados mockados
- Paginação compatível com GitLab
- Headers de resposta similares ao GitLab
- Endpoints para projetos, merge requests e commits

## 📋 Requisitos

- Python 3.7+
- FastAPI
- Uvicorn
- typing
- uuid

## 🛠️ Instalação

1. Clone o repositório:

```bash
git clone [URL_DO_REPOSITÓRIO]
```

2. Instale as dependências:

```bash
pip install fastapi uvicorn typing uuid
```

3. Execute a aplicação:

```bash
python main.py
```

Por padrão, a API estará disponível em `http://localhost:8000`

## 📚 Endpoints Disponíveis

### 1. Listar Projetos

```
GET /api/v4/projects
```

**Parâmetros de Query:**

- `page` (opcional): Número da página (default: 1)
- `per_page` (opcional): Itens por página (default: 20, max: 100)

**Exemplo de Resposta:**

```json
[
  {
    "id": 1,
    "name": "Project 1",
    "description": "This is a mock project 1 for testing",
    "web_url": "https://gitlab.example.com/project/1",
    "created_at": "2024-01-01T00:00:00",
    "last_activity_at": "2024-01-15T00:00:00",
    "visibility": "private",
    "default_branch": "main",
    "star_count": 42,
    "forks_count": 7
  }
]
```

### 2. Listar Merge Requests de um Projeto

```
GET /api/v4/projects/{project_id}/merge_requests
```

**Parâmetros:**

- `project_id`: ID do projeto (path parameter)
- `page` (opcional): Número da página (query parameter)
- `per_page` (opcional): Itens por página (query parameter)

**Exemplo de Resposta:**

```json
[
  {
    "id": 1,
    "iid": 1,
    "project_id": 1,
    "title": "Feature: Implement new functionality 1",
    "description": "This MR implements feature 1",
    "state": "opened",
    "merged_by": {
      "id": 5,
      "name": "User 5"
    },
    "merged_at": "2024-01-16T00:00:00",
    "created_at": "2024-01-15T00:00:00",
    "updated_at": "2024-01-15T12:00:00",
    "target_branch": "main",
    "source_branch": "feature/branch-1"
  }
]
```

### 3. Listar Commits de um Merge Request

```
GET /api/v4/projects/{project_id}/merge_requests/{mr_iid}/commits
```

**Parâmetros:**

- `project_id`: ID do projeto (path parameter)
- `mr_iid`: IID do merge request (path parameter)
- `page` (opcional): Número da página (query parameter)
- `per_page` (opcional): Itens por página (query parameter)

**Exemplo de Resposta:**

```json
[
  {
    "id": "uuid-string",
    "short_id": "short-uuid",
    "title": "commit: changes for feature 1 - 1",
    "author_name": "User 1",
    "author_email": "user1@example.com",
    "created_at": "2024-01-15T00:00:00",
    "message": "feat: implement changes for feature 1 - 1",
    "parent_ids": ["parent-uuid"]
  }
]
```

### 4. Listar Commits do Repositório

```
GET /api/v4/projects/{project_id}/repository/commits
```

**Parâmetros:**

- `project_id`: ID do projeto (path parameter)
- `page` (opcional): Número da página (query parameter)
- `per_page` (opcional): Itens por página (query parameter)

## 📝 Headers de Resposta

Todos os endpoints retornam os seguintes headers de paginação:

- `X-Total`: Total de itens disponíveis
- `X-Total-Pages`: Total de páginas
- `X-Per-Page`: Itens por página
- `X-Page`: Página atual
- `X-Next-Page`: Próxima página (vazio se não houver)
- `X-Prev-Page`: Página anterior (vazio se não houver)

## 🔧 Geração de Dados Mock

Os dados são gerados automaticamente quando a aplicação inicia:

- 100 projetos mockados
- 5-15 merge requests por projeto
- 1-5 commits por merge request
- 20-50 commits por repositório

### Estrutura dos Dados Mockados

- **Projetos**: Inclui informações básicas como nome, descrição, visibilidade e métricas
- **Merge Requests**: Estado, branches, datas de criação/atualização
- **Commits**: Autor, mensagem, datas e IDs

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: amazing feature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## ⚠️ Limitações

- Esta é uma API mock e não replica todas as funcionalidades do GitLab
- Os dados são gerados aleatoriamente e reiniciados quando a aplicação é reiniciada
- Alguns campos presentes na API real do GitLab podem estar ausentes

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
