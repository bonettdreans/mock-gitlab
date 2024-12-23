from fastapi import FastAPI, Query, Path, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
import random
from datetime import datetime, timedelta
import uuid

app = FastAPI()


def generate_mock_data():
    # Gera projetos mockados primeiro para ter IDs base
    projects = []
    for i in range(100):
        project_id = i + 1  # IDs sequenciais para garantir consistência
        namespace_id = random.randint(1, 20)
        created_date = datetime.now() - timedelta(days=random.randint(1, 365))
        last_activity = created_date + timedelta(days=random.randint(1, 30))

        project = {
            "id": project_id,
            "description": f"This is a mock project {project_id} for testing",
            "name": f"Project {project_id}",
            "name_with_namespace": f"Namespace {namespace_id} / Project {project_id}",
            "path": f"project-{project_id}",
            "path_with_namespace": f"namespace-{namespace_id}/project-{project_id}",
            "created_at": created_date.isoformat(),
            "default_branch": "main",
            "ssh_url_to_repo": f"git@gitlab.example.com:namespace-{namespace_id}/project-{project_id}.git",
            "http_url_to_repo": f"https://gitlab.example.com/namespace-{namespace_id}/project-{project_id}.git",
            "web_url": f"https://gitlab.example.com/namespace-{namespace_id}/project-{project_id}",
            "readme_url": f"https://gitlab.example.com/namespace-{namespace_id}/project-{project_id}/-/blob/main/README.md",
            "forks_count": random.randint(0, 50),
            "avatar_url": f"https://gitlab.example.com/uploads/project-avatars/{project_id}.png",
            "star_count": random.randint(0, 100),
            "last_activity_at": last_activity.isoformat(),
            "namespace_id": namespace_id
        }
        projects.append(project)

    # Gera commits com referências válidas aos projetos
    commits = {}
    all_commits = []  # Lista para manter todos os commits para referência
    commit_counter = 1  # Contador global para IDs únicos de commits

    for project in projects:
        project_commits = []
        num_commits = random.randint(20, 50)

        for _ in range(num_commits):
            authored_date = datetime.now() - timedelta(days=random.randint(1, 365))
            committed_date = authored_date + \
                timedelta(minutes=random.randint(1, 60))
            # ID sequencial para garantir unicidade
            commit_id = str(commit_counter)

            commit = {
                "id": commit_id,
                "short_id": commit_id[:8],
                "created_at": authored_date.isoformat(),
                "title": f"feat: implement changes {commit_counter}",
                "message": f"feat: implement changes {commit_counter}\n\nDetailed description of changes",
                "author_name": f"User {random.randint(1, 10)}",
                "author_email": f"user{random.randint(1, 10)}@example.com",
                "authored_date": authored_date.isoformat(),
                "committer_name": f"User {random.randint(1, 10)}",
                "committer_email": f"user{random.randint(1, 10)}@example.com",
                "committed_date": committed_date.isoformat(),
                "web_url": f"https://gitlab.example.com/namespace-{project['namespace_id']}/project-{project['id']}/-/commit/{commit_id}",
                "project_id": project["id"]  # Referência válida ao projeto
            }
            project_commits.append(commit)
            all_commits.append(commit)
            commit_counter += 1

        commits[project["id"]] = project_commits

    # Gera MRs com referências válidas aos projetos e commits
    merge_requests = {}
    mr_commits = {}  # Relacionamento N:N entre MRs e commits
    mr_global_id = 1

    for project in projects:
        project_mrs = []
        mr_commits[project["id"]] = {}
        project_commit_pool = commits[project["id"]]

        for j in range(random.randint(5, 15)):
            # Seleciona commits do próprio projeto
            num_commits = random.randint(1, min(5, len(project_commit_pool)))
            selected_commits = random.sample(project_commit_pool, num_commits)

            # Usa o commit mais recente para definir as datas do MR
            latest_commit_date = max(
                datetime.fromisoformat(commit["committed_date"])
                for commit in selected_commits
            )

            created_date = latest_commit_date + \
                timedelta(hours=random.randint(1, 24))
            updated_date = created_date + \
                timedelta(hours=random.randint(1, 48))
            merged_date = updated_date + \
                timedelta(hours=random.randint(1, 24)) if random.choice(
                    [True, False]) else None
            closed_date = merged_date if merged_date else (
                updated_date +
                timedelta(hours=random.randint(1, 24)) if random.choice(
                    [True, False]) else None
            )

            state = "merged" if merged_date else (
                "closed" if closed_date else "opened")

            mr = {
                "id": mr_global_id,
                "iid": j + 1,
                "project_id": project["id"],  # Referência válida ao projeto
                "title": f"Feature: Implement new functionality {j + 1}",
                "description": f"This MR implements feature {j + 1}",
                "state": state,
                "created_at": created_date.isoformat(),
                "updated_at": updated_date.isoformat(),
                "merged_at": merged_date.isoformat() if merged_date else None,
                "closed_at": closed_date.isoformat() if closed_date else None,
                "target_branch": "main",
                "source_branch": f"feature/branch-{j + 1}",
                "user_notes_count": random.randint(0, 20),
                "upvotes": random.randint(0, 10),
                "downvotes": random.randint(0, 5),
                # Mesmo projeto para simplificar
                "source_project_id": project["id"],
                "target_project_id": project["id"],
                "draft": random.choice([True, False]),
                "work_in_progress": random.choice([True, False]),
                "merge_status": random.choice(["can_be_merged", "cannot_be_merged"]),
                # Usa o ID do último commit selecionado
                "sha": selected_commits[-1]["id"]
            }
            project_mrs.append(mr)

            # Cria relacionamentos entre MR e commits
            mr_commit_list = []
            for commit in selected_commits:
                mr_commit = {
                    "commit_id": commit["id"],  # Referência válida ao commit
                    "iid": mr["iid"],
                    "merge_request_id": mr["id"],  # Referência válida ao MR
                    # Referência válida ao projeto
                    "project_id": project["id"],
                    "committed_date": commit["committed_date"],
                    "state": mr["state"],
                    "merged_at": merged_date.isoformat() if merged_date else None
                }
                mr_commit_list.append(mr_commit)

            mr_commits[project["id"]][mr["iid"]] = mr_commit_list
            mr_global_id += 1

        merge_requests[project["id"]] = project_mrs

    return projects, merge_requests, commits, mr_commits


# Gera dados mockados ao iniciar a aplicação
projects, merge_requests, commits, mr_commits = generate_mock_data()


@app.get("/api/v4/projects")
async def get_projects(
    per_page: Optional[int] = Query(
        20, description="Número de items por página", ge=1, le=100)
):
    paginated_projects = projects[:per_page]
    headers = {
        "X-Total": str(len(projects)),
        "X-Per-Page": str(per_page),
        "X-Page": "1",
        "X-Total-Pages": str((len(projects) + per_page - 1) // per_page)
    }
    return JSONResponse(content=paginated_projects, headers=headers)


@app.get("/api/v4/projects/{project_id}")
async def get_project(project_id: int = Path(..., description="ID do projeto")):
    project = next((p for p in projects if p["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return project


@app.get("/api/v4/projects/{project_id}/merge_requests")
async def get_merge_requests(
    project_id: int = Path(..., description="ID do projeto"),
    state: Optional[str] = Query(
        None, description="Estado do MR (opened, closed, merged, all)"),
    target_branch: Optional[str] = Query(None, description="Branch alvo"),
    per_page: Optional[int] = Query(
        20, description="Número de items por página", ge=1, le=100)
):
    if project_id not in merge_requests:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    project_mrs = merge_requests[project_id]
    filtered_mrs = project_mrs.copy()

    if state and state != 'all':
        filtered_mrs = [mr for mr in filtered_mrs if mr['state'] == state]

    if target_branch:
        filtered_mrs = [
            mr for mr in filtered_mrs if mr['target_branch'] == target_branch]

    total_items = len(filtered_mrs)
    paginated_mrs = filtered_mrs[:per_page]

    headers = {
        "X-Total": str(total_items),
        "X-Per-Page": str(per_page),
        "X-Page": "1",
        "X-Total-Pages": str((total_items + per_page - 1) // per_page)
    }
    return JSONResponse(content=paginated_mrs, headers=headers)


@app.get("/api/v4/projects/{project_id}/merge_requests/{mr_iid}")
async def get_merge_request(
    project_id: int = Path(..., description="ID do projeto"),
    mr_iid: int = Path(..., description="IID do Merge Request")
):
    if project_id not in merge_requests:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    mr = next(
        (mr for mr in merge_requests[project_id] if mr["iid"] == mr_iid), None)
    if not mr:
        raise HTTPException(
            status_code=404, detail="Merge Request não encontrado")
    return mr


@app.get("/api/v4/projects/{project_id}/merge_requests/{mr_iid}/commits")
async def get_merge_request_commits(
    project_id: int = Path(..., description="ID do projeto"),
    mr_iid: int = Path(..., description="IID do Merge Request")
):
    if project_id not in mr_commits or mr_iid not in mr_commits[project_id]:
        raise HTTPException(
            status_code=404, detail="Merge Request não encontrado")
    return mr_commits[project_id][mr_iid]


@app.get("/api/v4/projects/{project_id}/repository/commits")
async def get_project_commits(
    project_id: int = Path(..., description="ID do projeto"),
    per_page: Optional[int] = Query(
        20, description="Número de items por página", ge=1, le=100)
):
    if project_id not in commits:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    project_commits = commits[project_id]
    sorted_commits = sorted(
        project_commits,
        key=lambda x: datetime.fromisoformat(x["committed_date"]),
        reverse=True
    )

    total_items = len(sorted_commits)
    paginated_commits = sorted_commits[:per_page]

    headers = {
        "X-Total": str(total_items),
        "X-Per-Page": str(per_page),
        "X-Page": "1",
        "X-Total-Pages": str((total_items + per_page - 1) // per_page)
    }
    return JSONResponse(content=paginated_commits, headers=headers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
