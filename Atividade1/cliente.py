import socket
import json

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT)) #com o connect ele se conecta ao host e a porta

dados = client_socket.recv(1024).decode() #aqui ele recebe os dados do server
perguntas = json.loads(dados) #aqui ele desserializa os dados enviados pelo server

respostas = []
for p in perguntas: #aqui ele printa as perguntas e as opções que ele recebe do server
    print(p["pergunta"]) 
    for opcao in p["opcoes"]:
        print(opcao)
    resposta = input("Sua resposta: ").strip().upper() #aqui é escrito a sua resposta
    respostas.append(resposta)

client_socket.sendall(json.dumps(respostas).encode()) #aqui ele envia as respostas de novo para o server

feedback = client_socket.recv(1024).decode() #aqui ele recebe o feedback
feedback = json.loads(feedback)

print("\nResultado:")
print(f"Acertos: {feedback['acertos']}")
for detalhe in feedback["detalhes"]:
    print(detalhe)

client_socket.close()
