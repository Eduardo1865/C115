import socket
import json

perguntas = [
    {
        "pergunta": "qual é a capital da Letônia?",
        "opcoes": ["A) Riga", "B) Londres", "C) Roma", "D) Madrid"],
        "resposta_certa": "A"
    },
    {
        "pergunta": "quando o primeiro jogo da franquia sonic foi lançado?",
        "opcoes": ["A) 1991", "B) 900BC", "C) 2020", "D) 1994"],
        "resposta_certa": "A"
    },
    {
        "pergunta": "quando o INATEL foi fundado?",
        "opcoes": ["A) 1963", "B) 1965", "C) 2020", "D) 1994"],
        "resposta_certa": "B"
    }
]

HOST = '127.0.0.1' #só aceita conexões locais (mesma maquina)
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #aqui é criado um socket TCP por conta do SOCK_STREAM
server_socket.bind((HOST, PORT))                                
server_socket.listen(1) #ouvindo 1 cliente (o listen habilita o socket para aceitar o numero de clientes passado)
print(f"servidor aguarda conexão em {HOST}:{PORT}")

conn, addr = server_socket.accept() #o programa para aqui até alguem se conectar
print(f"Conexão estabelecida com {addr}") #conn -> novo socket dedicado a conexão com o cliente
                                          #addr -> ip do cliente e porta do cliente


dados_perguntas = json.dumps(perguntas) #serializar
conn.sendall(dados_perguntas.encode()) #sendall -> envia dados para o cliente


respostas_cliente = conn.recv(1024).decode() # recv de receive que significa que o server vai receber a resposta
respostas_cliente = json.loads(respostas_cliente) #desserializa


resultados = []
acertos = 0
for i, resp in enumerate(respostas_cliente): #aqui com o enumerate eu pego o indice e o conteudo da resposta
    correta = perguntas[i]["resposta_certa"]
    if resp == correta:
        resultados.append(f"Questão {i+1}: ACERTOU")
        acertos += 1
    else:
        resultados.append(f"Questão {i+1}: ERROU")


feedback = {"acertos": acertos, "detalhes": resultados}
conn.sendall(json.dumps(feedback).encode())

conn.close()
server_socket.close()
