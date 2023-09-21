# API de Controle Escolar - Atividade avaliativa 
# Aluno: Rafael Rodrigues - Ads 2º Semestre - Senai Gaspar Ricardo júnior


Esta é uma API de Controle Escolar que permite gerenciar tarefas, alunos e disciplinas. Ela oferece operações CRUD para cada uma dessas entidades, bem como a capacidade de consultar as tarefas de um aluno.

## Funcionalidades Principais

- **GET /tasks**: Retorna a lista de todas as tarefas.
- **POST /tasks**: Cria uma nova tarefa.
- **GET /tasks/{id}**: Retorna detalhes de uma tarefa específica.
- **PUT /tasks/{id}**: Atualiza os detalhes de uma tarefa específica.
- **DELETE /tasks/{id}**: Exclui uma tarefa específica.

- **GET /students**: Retorna a lista de todos os alunos.
- **POST /students**: Cria um novo aluno.
- **GET /students/{id}**: Retorna detalhes de um aluno específico.
- **PUT /students/{id}**: Atualiza os detalhes de um aluno específico.
- **DELETE /students/{id}**: Exclui um aluno específico.

- **GET /disciplines**: Retorna a lista de todas as disciplinas.
- **POST /disciplines**: Cria uma nova disciplina.
- **GET /disciplines/{id}**: Retorna detalhes de uma disciplina específica.
- **PUT /disciplines/{id}**: Atualiza os detalhes de uma disciplina específica.
- **DELETE /disciplines/{id}**: Exclui uma disciplina específica.

- **GET /students/{student_id}/disciplines**: Retorna as disciplinas de um aluno específico.

## Como Usar

1. Clone este repositório para sua máquina local:

```shell
git https://github.com/RafaelRodrigues44/controle_de_disciplinas_e_tarefas.git
cd seu-repositorio
python -m venv venv
source venv/bin/activate  # No Windows, use "venv\Scripts\activate"
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

