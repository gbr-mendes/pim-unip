# Dashboard do Professor

## Visão Geral

A visão do professor foi implementada seguindo o padrão do projeto, com foco na exibição das disciplinas atribuídas organizadas por curso. O professor pode visualizar, buscar e filtrar suas disciplinas de forma intuitiva.

## Estrutura de Arquivos

```
view/professor/
├── __init__.py
├── dashboard.py
└── components/
    ├── __init__.py
    ├── discipline_components.py
    ├── search_filter.py
    └── stats_widget.py
```

## Funcionalidades

### 1. Dashboard Principal (`dashboard.py`)
- **Carregamento de Dados**: Busca disciplinas e cursos via WebSocket
- **Organização por Curso**: Agrupa disciplinas do professor por curso
- **Filtros Dinâmicos**: Integração com busca e filtros
- **Tratamento de Erros**: Estados vazios e mensagens de erro

### 2. Componentes Visuais (`components/`)

#### `discipline_components.py`
- **DisciplineCard**: Card clicável para cada disciplina com informações básicas
- **CourseSection**: Seção expansível que agrupa disciplinas por curso
- **EmptyState**: Componente para estados vazios (sem dados, sem resultados)

#### `search_filter.py`
- **SearchAndFilterWidget**: Barra de busca por nome e filtro por curso
- **Busca em Tempo Real**: Filtragem automática conforme o usuário digita
- **Filtros Dinâmicos**: Opções de curso baseadas nas disciplinas do professor

#### `stats_widget.py`
- **StatsWidget**: Exibe estatísticas rápidas do professor
- **Métricas**: Total de disciplinas, cursos e disciplina mais recente
- **Atualização Dinâmica**: Se atualiza conforme filtros são aplicados

## Integração com o Sistema

### Navegação
O dashboard do professor é acessado através do arquivo `client.py` quando um usuário com role "professor" faz login.

### Dados
- **Disciplinas**: Carregadas via `discipline_controller.listar_disciplinas()`
- **Cursos**: Carregados via `course_controller.listar_cursos()`
- **Professor**: Dados do usuário logado via `session.get_usuario()`

### Filtros
O sistema de filtros permite:
- **Busca por Nome**: Filtra disciplinas por nome
- **Filtro por Curso**: Mostra apenas disciplinas de um curso específico
- **Combinação**: Ambos os filtros podem ser usados simultaneamente

## Fluxo de Dados

1. **Login**: Professor faz login e é redirecionado para o dashboard
2. **Carregamento**: Sistema busca todas as disciplinas e cursos
3. **Filtragem**: Filtra disciplinas atribuídas ao professor logado
4. **Organização**: Agrupa disciplinas por curso
5. **Exibição**: Mostra cards clicáveis organizados em seções por curso

## Estados da Interface

### Estados Normais
- **Com Dados**: Exibe seções de curso com cards de disciplinas
- **Busca Ativa**: Filtra e atualiza a visualização em tempo real

### Estados de Erro/Vazio
- **Sem Disciplinas**: Mostra mensagem amigável indicando que não há disciplinas atribuídas
- **Busca Sem Resultados**: Indica que nenhuma disciplina corresponde aos filtros
- **Erro de Conexão**: Mostra erro ao carregar dados do servidor

## Próximos Passos

O sistema está preparado para a implementação do gerenciamento de disciplinas. O callback `on_disciplina_click` já está definido e pode ser expandido para:

1. **Navegação**: Abrir tela de gestão da disciplina específica
2. **Modal/Popup**: Mostrar detalhes e opções de gestão
3. **Edição Inline**: Permitir edição rápida de informações básicas

## Padrões Seguidos

- **Componentes Reutilizáveis**: Cards e widgets modularizados
- **Separação de Responsabilidades**: Lógica separada da apresentação
- **Tratamento de Erros**: Estados apropriados para diferentes cenários
- **Responsividade**: Interface adaptável e expansível
- **Consistência Visual**: Seguindo o padrão do sistema admin existente