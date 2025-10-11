from websocket_server import WebsocketServer
import json
from model.usuarios_model import autenticar_usuario

def receber_mensagem(client, server, message):
    data = json.loads(message)

    if data["action"] == "login":
        user = data["username"]
        pwd = data["password"]

        usuario = autenticar_usuario(user, pwd)
        if usuario:
            resposta = {
                "status": "ok",
                "message": "Login bem-sucedido",
                "user": {
                    "username": usuario["username"],
                    "role": usuario["role"]
                }
            }
        else:
            resposta = {"status": "error", "message": "Credenciais inválidas"}

        server.send_message(client, json.dumps(resposta))

if __name__ == "__main__":
    server = WebsocketServer(host="0.0.0.0", port=8080)
    server.set_fn_message_received(receber_mensagem)
    print("Servidor rodando na porta 8080...")
    server.run_forever()
