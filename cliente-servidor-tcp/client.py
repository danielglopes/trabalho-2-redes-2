"""
Exercício 1: Cliente-Servidor TCP
Cliente que envia mensagem válida e recebe confirmação do servidor.

Participante:
    - Joana de Oliveira Rocha
"""

import socket
import sys

# Configurações de conexão
HOST = '127.0.0.1'  # endereço do servidor
PORT = 5000         # porta do servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção


def main():
    """
    Conecta ao servidor, lê input do usuário, valida não vazio, envia e imprime resposta.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f'❌ Não foi possível conectar a {HOST}:{PORT}')
            sys.exit(1)

        # lê mensagem do usuário
        mensagem = input('✉️  Digite sua mensagem: ').strip()
        # valida mensagem vazia
        if not mensagem:
            print('Erro: mensagem vazia não é permitida')
            return

        # envia dados ao servidor
        s.sendall(mensagem.encode('utf-8'))
        # aguarda resposta
        try:
            resposta = s.recv(BUFFER_SIZE).decode('utf-8')
        except Exception as e:
            print(f'❌ Erro ao receber resposta: {e}')
            return

        # exibe confirmação do servidor
        print(f'✅ Resposta do servidor: {resposta}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # mensagem amigável ao usuário
        print('\n🔴 Cliente encerrado pelo usuário')
        sys.exit(0)