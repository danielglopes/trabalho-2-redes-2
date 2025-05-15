"""
Exercício 4: Cliente de Hora TCP
Cliente que solicita a hora ao servidor e exibe no console.

Participantes:
    - Daniel Gonçalves Lopes
    - Joana de Oliveira Rocha
    - João Victor Almeida
"""

import socket
import sys

# Configurações de conexão
SERVER_HOST = '127.0.0.1'  # endereço do servidor
SERVER_PORT = 7000         # mesma porta do servidor
ENCODING = 'utf-8'
BUFFER_SIZE = 1024

def main():
    """
    Conecta ao servidor, envia requisição GET_TIME e imprime a hora recebida.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((SERVER_HOST, SERVER_PORT))
        except ConnectionRefusedError:
            print(f'❌ Não foi possível conectar a {SERVER_HOST}:{SERVER_PORT}')
            sys.exit(1)

        # Envia comando para solicitar horário
        req = 'GET_TIME'
        sock.sendall(req.encode(ENCODING))

        # Aguarda resposta do servidor
        data = sock.recv(BUFFER_SIZE)
        if not data:
            print('❌ Servidor não enviou dados.')
            sys.exit(1)

        hora = data.decode(ENCODING)
        print(f'🕒 Hora atual recebida do servidor: {hora}')

if __name__ == '__main__':
    main()