#!/usr/bin/env python3
"""
Script de teste para verificar a estrutura do dashboard do professor
"""

import sys
import os

# Adiciona o diretório do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todos os imports estão funcionando"""
    try:
        print("🔄 Testando imports...")
        
        # Testa import do dashboard principal
        from view.professor.dashboard import criar_dashboard_professor
        print("✅ Dashboard principal importado com sucesso")
        
        # Testa imports dos componentes
        from view.professor.components.discipline_components import DisciplineCard, CourseSection, EmptyState
        print("✅ Componentes de disciplina importados com sucesso")
        
        from view.professor.components.search_filter import SearchAndFilterWidget
        print("✅ Widget de busca e filtro importado com sucesso")
        
        from view.professor.components.stats_widget import StatsWidget
        print("✅ Widget de estatísticas importado com sucesso")
        
        # Testa imports dos controllers
        from controller.discipline_controller import listar_disciplinas
        from controller.course_controller import listar_cursos
        print("✅ Controllers importados com sucesso")
        
        print("🎉 Todos os imports funcionaram corretamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_file_structure():
    """Verifica se a estrutura de arquivos está correta"""
    print("\n🔄 Verificando estrutura de arquivos...")
    
    required_files = [
        "view/professor/__init__.py",
        "view/professor/dashboard.py",
        "view/professor/components/__init__.py",
        "view/professor/components/discipline_components.py",
        "view/professor/components/search_filter.py",
        "view/professor/components/stats_widget.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - ARQUIVO NÃO ENCONTRADO")
            all_exist = False
    
    if all_exist:
        print("🎉 Todos os arquivos necessários estão presentes!")
    else:
        print("⚠️ Alguns arquivos estão faltando!")
    
    return all_exist

def test_data_structure():
    """Verifica se os dados de teste estão adequados"""
    print("\n🔄 Verificando dados de teste...")
    
    try:
        import json
        
        # Verifica usuários
        with open("data/usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)
        
        professores = [u for u in usuarios if u.get("role") == "professor"]
        print(f"✅ Encontrados {len(professores)} professores nos dados")
        
        # Verifica disciplinas
        with open("data/disciplinas.json", "r", encoding="utf-8") as f:
            disciplinas = json.load(f)
        
        disciplinas_com_professor = [d for d in disciplinas if d.get("professor_id")]
        print(f"✅ Encontradas {len(disciplinas_com_professor)} disciplinas com professor atribuído")
        
        # Verifica cursos
        with open("data/cursos.json", "r", encoding="utf-8") as f:
            cursos = json.load(f)
        
        print(f"✅ Encontrados {len(cursos)} cursos nos dados")
        
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Arquivo de dados não encontrado: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao ler JSON: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🧪 TESTE DO DASHBOARD DO PROFESSOR")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Teste 1: Estrutura de arquivos
    if test_file_structure():
        tests_passed += 1
    
    # Teste 2: Imports
    if test_imports():
        tests_passed += 1
    
    # Teste 3: Dados
    if test_data_structure():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {tests_passed}/{total_tests} testes passaram")
    
    if tests_passed == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM! O dashboard do professor está pronto para uso.")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Iniciar o servidor: python server.py")
        print("2. Iniciar o cliente: python client.py")
        print("3. Fazer login com um professor (ex: aldy@email.com / 1234)")
        print("4. Testar a funcionalidade do dashboard")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    main()