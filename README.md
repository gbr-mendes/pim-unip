# Sistema Educacional – Setup C++ no Windows

Este projeto combina **Python (Tkinter + JSON)** com **módulos C++ estruturado**, compilados como **DLLs** para serem usadas no Python via `ctypes`.

---

## 1. Instalação do Compilador

1. Baixe e instale **MSYS2**: [https://www.msys2.org](https://www.msys2.org)
2. Atualize os pacotes:

```bash
pacman -Syu
```

3. Feche e reabra o terminal **MSYS2 UCRT64**.
4. Instale o compilador MinGW-w64 (UCRT64, 64 bits):

```bash
pacman -S mingw-w64-ucrt-x86_64-gcc
```

5. Confirme a instalação:

```bash
g++ --version
```

Você deve ver algo como:

```
g++.exe (Rev8, Built by MSYS2 project) 15.2.0
```

---

## 2. Estrutura de Pastas

```
sistema-educacional/
│
├── .venv/                  # Virtualenv Python
├── controller/             # Controllers Python
├── cpp_modules/            # Código C++ e DLLs
│   ├── usuarios.cpp
│   ├── ordenacao.cpp
│   ├── busca.cpp
│   └── relatorios.cpp
├── data/                   # JSONs, DB simulados
├── model/                  # Models Python
├── view/                   # Views Python (Tkinter)
```

---

## 3. Compilando as DLLs

Entre na pasta **cpp\_modules** pelo terminal **MSYS2 UCRT64**:

```bash
cd /c/Users/Gabri/Documents/Pessoal/unip/pim-unip/sistema-educacional/cpp_modules
```

Compile cada módulo:

```bash
g++ -shared -o libusuarios.dll usuarios.cpp -static -static-libgcc -static-libstdc++
g++ -shared -o libordenacao.dll ordenacao.cpp -static -static-libgcc -static-libstdc++
g++ -shared -o libbusca.dll busca.cpp -static -static-libgcc -static-libstdc++
g++ -shared -o librelatorios.dll relatorios.cpp -static -static-libgcc -static-libstdc++
```

**Observações importantes:**

* Use **sempre** o terminal `MSYS2 UCRT64`.
* A flag `-static` evita dependências externas como `libwinpthread-1.dll`.
* DLLs compiladas ficarão dentro de `cpp_modules/` e podem ser usadas no Python.

---

## 4. Carregando DLLs no Python

Exemplo (`usuarios_model.py`):

```python
import os
import json
from ctypes import CDLL, c_char_p

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DLL_PATH = os.path.join(BASE_DIR, "../cpp_modules/libusuarios.dll")

lib = CDLL(DLL_PATH)
lib.carregar_usuarios_json.argtypes = [c_char_p]
lib.carregar_usuarios_json.restype = c_char_p

USUARIOS_FILE = b"data/usuarios.json"

def carregar_usuarios():
    conteudo = lib.carregar_usuarios_json(USUARIOS_FILE)
    usuarios = json.loads(conteudo.decode("utf-8"))
    return usuarios
```

---

## 5. Dicas

* **Sempre compile em UCRT64**, não no terminal MSYS ou MinGW32.
* Use nomes padronizados `lib<nome>.dll` para facilitar o carregamento no Python.
* DLLs estão em **cpp\_modules/**; JSONs em **data/**; Python em **controller**, **model**, **view**.


## Start do Projeto

O projeto possui **client** e **server**, ambos precisam estar rodando para que a aplicação funcione corretamente.

Documentação completa do sistema (com diagramas): consulte `docs/sistema-educacional.md`.

### Passos:

1. Ative o ambiente virtual Python:

   ```bash
   .venv\Scripts\activate
   ```
2. Suba o **server**:

   ```bash
   python server.py
   ```
3. Suba o **client** (em outra janela do terminal):

   ```bash
   python client.py
   ```

> Certifique-se de que o server está rodando antes do client.
