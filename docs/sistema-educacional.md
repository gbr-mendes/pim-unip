# Sistema Educacional — Documentação

Este documento descreve a arquitetura, dados, fluxos e API do sistema educacional localizado em `sistema-educacional/`. Inclui diagramas Mermaid (renderizam no GitHub e VS Code) para casos de uso, relações de dados e fluxos principais.

## Visão geral

- Cliente desktop em Python usando CustomTkinter (UI)
- Comunicação via WebSocket (JSON) entre cliente e servidor
- Servidor Python gerencia ações e persiste dados
- Persistência em arquivos JSON, acessados via módulo C++ exposto como DLL no Windows

Principais recursos (admin):
- Autenticação de usuários
- Cadastro/listagem de Administradores, Professores, Alunos
- Cadastro de Cursos, Disciplinas, Turmas
- Associações: Disciplina↔Curso, Professor↔Disciplina, Turma↔Curso, Aluno↔Turma, Disciplina↔Turma

## Arquitetura do sistema

```mermaid
flowchart LR
    subgraph UI[Cliente Desktop - CustomTkinter]
      LV[view/login_view.py]
      AD[view/admin/dashboard.py + tabs/*]
      CTRL[controller/*]
    end

    WSM[controller/websocket_manager.py - WebSocket cliente]

    subgraph S[Servidor Python]
      SVR[server.py - WebsocketServer]
      HANDLERS[Handlers de ações]
    end

    subgraph M[Model / Persistência]
      DA_PY[model/data_access.py]
      DA_DLL[cpp_modules/libdata_access.dll]
      JSON[(data/*.json)]
    end

    LV --> CTRL
    AD --> CTRL
    CTRL --> WSM --> SVR
    SVR --> HANDLERS --> DA_PY --> DA_DLL --> JSON
```

## Atores e casos de uso (alto nível)

```mermaid
flowchart TD
    Admin([👤 Administrador])
    Prof([👨‍🏫 Professor])
    Aluno([👨‍🎓 Aluno])

    subgraph Admin_UC["🔧 Administração do Sistema"]
        A1[Gerenciar Usuários]
        A2[Gerenciar Cursos]
        A3[Gerenciar Disciplinas]
        A4[Gerenciar Turmas]
        A5[Fazer Associações]
    end

    subgraph Prof_UC["📚 Gestão de Conteúdo"]
        P1[Dashboard Disciplinas]
        P2[Criar/Editar Módulos]
        P3[Criar/Editar Aulas]
        P4[Visualizar Estatísticas]
        P5[Buscar Conteúdo]
    end

    subgraph Aluno_UC["🎯 Aprendizado"]
        S1[Visualizar Disciplinas]
        S2[Acessar Módulos]
        S3[Assistir Aulas]
        S4[Acompanhar Progresso]
    end

    subgraph Auth_UC["🔐 Autenticação"]
        LOGIN[Login/Logout]
    end

    %% Conexões simplificadas
    Admin --> Admin_UC
    Prof --> Prof_UC
    Aluno --> Aluno_UC
    
    Admin --> Auth_UC
    Prof --> Auth_UC
    Aluno --> Auth_UC
```

**Status de Implementação:**
- ✅ **Administração**: Totalmente implementada
- ✅ **Professor**: Totalmente implementada  
- ✅ **Aluno**: Totalmente implementada

### Resumo das Funcionalidades

| Ator | Principais Responsabilidades | Status |
|------|----------------------------|---------|
| 👤 **Administrador** | • Cadastro de usuários (admin, professor, aluno)<br>• Gestão de cursos, disciplinas e turmas<br>• Associações entre entidades<br>• Controle total do sistema | ✅ Implementado |
| 👨‍🏫 **Professor** | • Dashboard com disciplinas atribuídas<br>• Criação de módulos didáticos<br>• Desenvolvimento de aulas<br>• Estatísticas de conteúdo | ✅ Implementado |
| 👨‍🎓 **Aluno** | • Dashboard com disciplinas matriculadas<br>• Visualização de módulos e aulas<br>• Acompanhamento de progresso<br>• Controle de conclusão de aulas | ✅ Implementado |

## Modelo de dados (Entidades e relações)

Arquivos JSON:
- `data/usuarios.json`
- `data/cursos.json`
- `data/disciplinas.json`
- `data/turmas.json`
- `data/modulos.json`
- `data/aulas.json`
- `data/progresso.json`

```mermaid
erDiagram
  USUARIO {
    string id PK
    string username
    string password
    string nome
    string sobrenome
    string role
    string email
  }

  CURSO {
    string id PK
    string nome
    string created_at
    string updated_at
  }

  DISCIPLINA {
    string id PK
    string nome
    string professor_id FK
    string curso_id FK
    string created_at
    string updated_at
  }

  TURMA {
    string id PK
    string nome
    string curso_id FK
    string created_at
    string updated_at
  }

  MODULO {
    string id PK
    string disciplina_id FK
    string nome
    string descricao
    int sequencia
    string created_at
    string updated_at
  }

  AULA {
    string id PK
    string modulo_id FK
    string titulo
    string conteudo
    int sequencia
    string created_at
    string updated_at
  }

  PROGRESSO {
    string id PK
    string aluno_id FK
    string aula_id FK
    boolean concluida
    string data_conclusao
    int tempo_gasto
  }

  USUARIO ||--o{ DISCIPLINA : "professor leciona"
  CURSO ||--o{ DISCIPLINA : "possui disciplinas"
  CURSO ||--o{ TURMA : "agrupa turmas"
  USUARIO ||--o{ TURMA : "aluno frequenta"
  TURMA }o--o{ DISCIPLINA : "tem disciplinas"
  DISCIPLINA ||--o{ MODULO : "contém módulos"
  MODULO ||--o{ AULA : "organiza aulas"
  USUARIO ||--o{ PROGRESSO : "aluno progride"
  AULA ||--o{ PROGRESSO : "aula tem progresso"
```

Notas:
- IDs são strings numéricas geradas aleatoriamente (`model/data_access.py::gerar_id`).
- Senhas são armazenadas em texto puro (apenas para fins didáticos; ver seção Segurança).

## Fluxos principais

### Fluxo de Login

```mermaid
sequenceDiagram
  autonumber
  participant UI as UI login_view
  participant CTRL as login_controller
  participant WSM as WebSocketManager
  participant SVR as server.py
  participant DA as data_access.py
  participant STORE as Arquivos JSON

  UI->>CTRL: tentar_login com usuário e senha
  CTRL->>WSM: enviar ação de login com credenciais
  WSM->>SVR: encaminhar mensagem via WebSocket
  SVR->>DA: autenticar_usuario com credenciais
  DA->>STORE: ler usuários
  DA-->>SVR: retorna usuário ou None
  SVR-->>WSM: resposta com status e dados
  WSM-->>CTRL: entregar resposta
  CTRL-->>UI: sucesso ou erro e redireciona por role
```

### Fluxo: Dashboard do Professor e Gestão de Conteúdo

```mermaid
sequenceDiagram
    autonumber
    participant UI as UI Professor Dashboard
    participant CTRL as professor/discipline_controller
    participant WSM as WebSocketManager
    participant SVR as server.py
    participant DA as data_access.py

    UI->>CTRL: carregar dashboard do professor
    CTRL->>WSM: listar_disciplinas do professor logado
    WSM->>SVR: buscar disciplinas por professor_id
    SVR->>DA: obter disciplinas do professor
    DA-->>SVR: lista de disciplinas
    SVR-->>WSM: disciplinas e estatísticas
    WSM-->>CTRL: dados das disciplinas
    CTRL-->>UI: exibir cards de disciplinas por curso

    alt criar módulo
        UI->>CTRL: criar_modulo com disciplina_id e dados
        CTRL->>WSM: solicitar criação de módulo
        WSM->>SVR: criar_modulo
        SVR->>DA: persistir módulo em modulos.json
        DA-->>SVR: confirmação
        SVR-->>UI: módulo criado com sucesso
    end

    alt criar aula
        UI->>CTRL: criar_aula com modulo_id e conteúdo
        CTRL->>WSM: solicitar criação de aula
        WSM->>SVR: criar_aula
        SVR->>DA: persistir aula em aulas.json
        DA-->>SVR: confirmação
        SVR-->>UI: aula criada com sucesso
    end
```

### Fluxo: Criar Turma e associar Curso/Disciplinas

```mermaid
sequenceDiagram
    autonumber
    participant UI as UI Admin Turmas
    participant CTRL as class_controller
    participant WSM as WebSocketManager
    participant SVR as server.py
    participant DA as data_access.py

    UI->>CTRL: criar_turma com nome e seleções
    CTRL->>WSM: solicitar criação de turma
    WSM->>SVR: enviar requisição criar_turma
    SVR->>DA: persistir turma em turmas.json
    DA-->>SVR: confirmação e id da turma
    SVR-->>WSM: retorna OK e id da turma
    
    alt curso selecionado
        CTRL->>WSM: solicitar associação turma ao curso
        WSM->>SVR: associar_turma_curso
        SVR->>DA: atualizar associação
        DA-->>SVR: confirmação
        SVR-->>WSM: status associação
    end
    
    loop para cada disciplina selecionada
        CTRL->>WSM: solicitar associação disciplina à turma
        WSM->>SVR: associar_disciplina_turma
        SVR->>DA: atualizar associação
        DA-->>SVR: confirmação
        SVR-->>WSM: status associação
    end
    
    WSM-->>CTRL: todas associações completas
    CTRL-->>UI: turma criada e associada com sucesso
```

```mermaid
sequenceDiagram
  autonumber
  participant UI as UI Admin Turmas
  participant CTRL as class_controller
  participant WSM as WebSocketManager
  participant SVR as server.py

  UI->>CTRL: criar_turma com nome e seleções
  CTRL->>WSM: solicitar criação de turma
  WSM->>SVR: enviar requisição criar_turma
  SVR-->>WSM: retorna OK e id da turma
  alt curso selecionado
    CTRL->>WSM: solicitar associação turma ao curso
    WSM->>SVR: associar turma ao curso
    SVR-->>WSM: status associação
  end
  loop para cada disciplina selecionada
    CTRL->>WSM: solicitar associação disciplina à turma
    WSM->>SVR: associar disciplina à turma
    SVR-->>WSM: status associação
  end
  CTRL-->>UI: exibir mensagem com sucessos e erros
```

### Fluxo: Gestão Completa de Conteúdo Didático

```mermaid
sequenceDiagram
    autonumber
    participant PROF as Professor
    participant UI as Interface Professor
    participant CTRL as Controllers
    participant WSM as WebSocket Manager
    participant SVR as Server
    participant DB as JSON Files

    Note over PROF,DB: Criação de Estrutura Didática
    
    PROF->>UI: Acessar disciplina
    UI->>CTRL: Carregar disciplina details
    CTRL->>WSM: listar_modulos_disciplina
    WSM->>SVR: request modules
    SVR->>DB: read modulos.json
    DB-->>SVR: modules data
    SVR-->>WSM: modules list
    WSM-->>CTRL: modules response
    CTRL-->>UI: Display modules
    
    PROF->>UI: Criar novo módulo
    UI->>CTRL: criar_modulo(disciplina_id, nome, descricao)
    CTRL->>WSM: send create_module
    WSM->>SVR: process create_module
    SVR->>DB: save to modulos.json
    DB-->>SVR: confirmation
    SVR-->>WSM: success response
    WSM-->>CTRL: module created
    CTRL-->>UI: Update module list
    
    PROF->>UI: Adicionar aulas ao módulo
    UI->>CTRL: criar_aula(modulo_id, titulo, conteudo)
    CTRL->>WSM: send create_aula
    WSM->>SVR: process create_aula
    SVR->>DB: save to aulas.json
    DB-->>SVR: confirmation
    SVR-->>WSM: success response
    WSM-->>CTRL: aula created
    CTRL-->>UI: Update aulas list
    
    Note over PROF,DB: Estrutura Didática Completa
```

## API (WebSocket JSON)

- Protocolo: WebSocket
- URL: definida por `WEBSOCKET_URL` em `.env` do cliente (ex.: `ws://localhost:8080`)
- Formato: mensagens JSON com `action` e campos específicos

Ações suportadas pelo servidor (`server.py`):

- Autenticação
  - `login` → req: {username, password} | resp: {status, message, user?}
- Cadastro
  - `cadastrar_admin` → {nome, sobrenome, email, senha}
  - `cadastrar_aluno` → {nome, sobrenome, email, senha}
  - `cadastrar_professor` → {nome, sobrenome, email, senha}
  - `cadastrar_curso` → {nome}
  - `cadastrar_disciplina` → {nome}
  - `criar_turma` → {nome}
- Listagem
  - `listar_admins` | `listar_alunos` | `listar_professores`
  - `listar_cursos` | `listar_disciplinas` | `listar_turmas`
- Gestão de Conteúdo Didático
  - `listar_modulos` | `listar_modulos_disciplina` → {disciplina_id?}
  - `criar_modulo` → {disciplina_id, nome, descricao?, ordem?}
  - `editar_modulo` → {id, nome?, descricao?, ordem?}
  - `excluir_modulo` → {id}
  - `listar_aulas` | `listar_aulas_modulo` → {modulo_id?}
  - `criar_aula` → {modulo_id, titulo, resumo, video_url?, ordem?}
  - `editar_aula` → {id, titulo?, resumo?, video_url?, ordem?}
  - `excluir_aula` → {id}
- Associações
  - `associar_disciplina_curso` → {id_disciplina, id_curso}
  - `atribuir_professor_disciplina` → {id_professor, id_disciplina}
  - `associar_turma_curso` → {id_turma, id_curso}
  - `atribuir_aluno_turma` → {id_aluno, id_turma}
  - `associar_disciplina_turma` → {id_disciplina, id_turma}
- Funcionalidades do Aluno
  - `listar_disciplinas_aluno` → {aluno_id}
  - `obter_progresso_aluno` → {aluno_id, disciplina_id?}
  - `marcar_aula_concluida` → {aluno_id, aula_id}
  - `obter_estatisticas_aluno` → {aluno_id}
  - `buscar_conteudo_aluno` → {aluno_id, termo_busca}

Padrão de resposta:
- Sucesso: `{ "status": "ok", "message"?: string, "data"?: any }`
- Erro: `{ "status": "error", "message": string }`

## Módulos principais

- UI (CustomTkinter)
  - `view/login_view.py`: tela de login (async via thread + spinner)
  - `view/admin/dashboard.py` e `view/admin/tabs/*`: CRUD/associações administrativas
  - `view/professor/dashboard.py`: interface do professor com gestão de disciplinas
  - `view/professor/discipline_management.py`: gerenciamento de conteúdo didático
  - `view/professor/components/*`: componentes especializados (stats, busca, dialogs, cards de disciplinas)
- Controllers (cliente)
  - `controller/*_controller.py`: validam inputs, montam mensagens, interpretam respostas, exibem mensagens para UI
    - `admin_controller.py`: operações administrativas gerais
    - `course_controller.py`: gestão de cursos
    - `discipline_controller.py`: gestão de disciplinas
    - `student_controller.py`: gestão de alunos
    - `professor_controller.py`: gestão de professores
    - `class_controller.py`: gestão de turmas
    - `modulo_controller.py`: gestão de módulos didáticos
    - `aula_controller.py`: gestão de aulas
    - `login_controller.py`: autenticação
  - `controller/websocket_manager.py`: singleton de conexão WebSocket, leitura `.env` (`WEBSOCKET_URL`)
- Servidor
  - `server.py`: mapeia `action` → handler; serializa respostas; roda `websocket_server` na porta 8080
- Model/Persistência
  - `model/data_access.py`: carrega/salva JSON via `libdata_access.dll` (C++)
  - `cpp_modules/libdata_access.dll`: implementação nativa de IO dos JSON
  - `data/*.json`: dados persistidos (usuarios, cursos, disciplinas, turmas, modulos, aulas, progresso)
- Sessão
  - `session.py`: gerenciamento de estado da sessão do usuário logado

### Detalhamento da Interface do Professor

A interface do professor representa um dos módulos mais complexos do sistema, oferecendo funcionalidades especializadas para gestão de conteúdo didático:

#### Dashboard Principal (`view/professor/dashboard.py`)
- **Lista de Disciplinas**: Exibe todas as disciplinas atribuídas ao professor em formato de cards visuais
- **Estatísticas por Disciplina**: Cada card mostra métricas como número de módulos, aulas e status de desenvolvimento
- **Ações Rápidas**: Botões para criar, editar, visualizar e gerenciar conteúdo de cada disciplina
- **Sistema de Busca**: Filtros por nome da disciplina e status de desenvolvimento

#### Gestão de Conteúdo (`view/professor/discipline_management.py`)
- **CRUD de Módulos**: Interface para criação, edição e exclusão de módulos didáticos
- **CRUD de Aulas**: Gestão de aulas dentro de cada módulo com validação de sequência
- **Validação de Campos**: Sistema robusto de validação para garantir integridade dos dados
- **Feedback Visual**: Mensagens de sucesso/erro para todas as operações

#### Componentes Especializados (`view/professor/components/`)
- `stats_widget.py`: Widget customizado para exibição de estatísticas
- `search_filter.py`: Componente de busca e filtros avançados
- `dialogs.py`: Diálogos modais padronizados para operações CRUD
- `discipline_components.py`: Cards informativos de disciplinas
- `modulo_components.py`: Interface de gestão de módulos e aulas

### Detalhamento da Interface do Aluno

A interface do aluno foi implementada para proporcionar uma experiência de aprendizado completa e intuitiva:

#### Dashboard Principal (`view/student/dashboard.py`)
- **Portal Personalizado**: Exibe informações do aluno e progresso acadêmico geral
- **Lista de Disciplinas**: Cards visuais das disciplinas em que o aluno está matriculado
- **Widget de Progresso**: Estatísticas em tempo real (total, concluídas, em andamento, não iniciadas)
- **Sistema de Busca e Filtros**: Localização rápida de disciplinas por nome ou status de progresso

#### Visualizador de Módulos (`view/student/components/module_viewer.py`)
- **Navegação Estruturada**: Interface organizada com sidebar para módulos e área de conteúdo para aulas
- **Visualização de Aulas**: Conteúdo expandível com texto completo das aulas
- **Controle de Progresso**: Botões para marcar aulas como concluídas
- **Informações Contextuais**: Dados do professor, curso e estatísticas de cada disciplina

#### Componentes do Aluno (`view/student/components/`)
- `discipline_card.py`: Cards informativos com progresso visual por disciplina
- `progress_widget.py`: Dashboard de estatísticas acadêmicas
- `search_filter.py`: Sistema de busca e filtros por status de progresso
- `module_viewer.py`: Interface completa para consumo de conteúdo educacional

### Controladores de Conteúdo

#### Módulo Controller (`controller/modulo_controller.py`)
Responsável por operações relacionadas a módulos didáticos:
- `criar_modulo()`: Criação de novos módulos com validação
- `listar_modulos_disciplina()`: Listagem de módulos por disciplina
- `atualizar_modulo()`: Edição de módulos existentes
- `excluir_modulo()`: Remoção de módulos com verificação de dependências

#### Aula Controller (`controller/aula_controller.py`)
Gerencia operações de aulas:
- `criar_aula()`: Criação de aulas com associação a módulos
- `listar_aulas_modulo()`: Listagem de aulas por módulo
- `atualizar_aula()`: Edição de conteúdo de aulas
- `excluir_aula()`: Remoção de aulas

### Estruturas de Dados

#### Módulos (`data/modulos.json`)
Estrutura para armazenamento de módulos didáticos:
```json
{
  "id": "string",
  "disciplina_id": "string", 
  "nome": "string",
  "descricao": "string",
  "sequencia": "number",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Aulas (`data/aulas.json`)
Estrutura para armazenamento de aulas:
```json
{
  "id": "string",
  "modulo_id": "string",
  "titulo": "string", 
  "conteudo": "string",
  "sequencia": "number",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Configuração e execução

Pré-requisitos:
- Windows (DLL fornecida: `cpp_modules/libdata_access.dll`)
- Python 3.10+

Instalação de dependências (na pasta `sistema-educacional/`):

```powershell
pip install -r requirements.txt
```

Configurar o cliente para apontar ao servidor local:
- Crie/edite `sistema-educacional/.env` com:
  - `WEBSOCKET_URL=ws://localhost:8080`

Executar servidor (WebSocket, porta 8080):

```powershell
python sistema-educacional/server.py
```

Executar cliente (UI):

```powershell
python sistema-educacional/client.py
```

## Segurança e limitações

- Senhas são armazenadas em texto puro nos JSON (apenas fins didáticos). Recomendações:
  - Usar hashing (bcrypt/argon2) e sal
  - Trocar WebSocket para WSS com TLS em produção
- Não há autenticação por sessão/token; cliente confia na resposta de login
- IDs randômicos simples podem colidir em grandes volumes (probabilidade baixa, mas possível)
- Não há validação forte de permissão no servidor (comentada em `handle_cadastrar_admin`) — reforçar RBAC

## Próximos passos sugeridos

- Adicionar hashing de senha e tokens de sessão
- Consolidar endpoint de criação de turma (permitir curso e disciplinas na mesma requisição)
- Padrão de validação e mensagens internacionalizadas
- Testes automatizados (unit/integration) para handlers e controllers
- Migração futura de JSON para um banco relacional (SQLite/PostgreSQL)

---

Seções de código relevantes:
- Servidor: `sistema-educacional/server.py`
- Cliente: `sistema-educacional/client.py`
- Controllers: `sistema-educacional/controller/*.py`
- UI: `sistema-educacional/view/*`
- Modelo: `sistema-educacional/model/data_access.py`
- Dados: `sistema-educacional/data/*.json`
