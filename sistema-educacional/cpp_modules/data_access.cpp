#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

extern "C" {
    // Função genérica para carregar qualquer arquivo JSON
    const char* carregar_json(const char* caminho) {
        static std::string conteudo;
        std::ifstream file(caminho);
        if (!file.is_open()) {
            conteudo = "[]";
            return conteudo.c_str();
        }
        std::stringstream buffer;
        buffer << file.rdbuf();
        conteudo = buffer.str();
        return conteudo.c_str();
    }

    // Função genérica para salvar em qualquer arquivo JSON
    bool salvar_json(const char* caminho, const char* conteudo) {
        std::ofstream file(caminho);
        if (!file.is_open()) {
            return false;
        }
        file << conteudo;
        return true;
    }

    // Funções específicas para cada tipo de dados
    const char* carregar_usuarios_json(const char* caminho) {
        return carregar_json(caminho);
    }

    const char* carregar_cursos_json(const char* caminho) {
        return carregar_json(caminho);
    }

    const char* carregar_disciplinas_json(const char* caminho) {
        return carregar_json(caminho);
    }

    const char* carregar_turmas_json(const char* caminho) {
        return carregar_json(caminho);
    }

    bool salvar_usuarios_json(const char* caminho, const char* conteudo) {
        return salvar_json(caminho, conteudo);
    }

    bool salvar_cursos_json(const char* caminho, const char* conteudo) {
        return salvar_json(caminho, conteudo);
    }

    bool salvar_disciplinas_json(const char* caminho, const char* conteudo) {
        return salvar_json(caminho, conteudo);
    }

    bool salvar_turmas_json(const char* caminho, const char* conteudo) {
        return salvar_json(caminho, conteudo);
    }
}
