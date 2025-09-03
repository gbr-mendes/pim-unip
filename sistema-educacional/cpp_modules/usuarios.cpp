#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

extern "C" {
    // Lê o arquivo JSON de usuários e retorna como string
    const char* carregar_usuarios_json(const char* caminho) {
        static std::string conteudo; // precisa ser static para não perder referência
        std::ifstream file(caminho);
        if (!file.is_open()) {
            conteudo = "[]"; // fallback caso não abra o arquivo
            return conteudo.c_str();
        }

        std::stringstream buffer;
        buffer << file.rdbuf();
        conteudo = buffer.str();
        return conteudo.c_str();
    }
}
