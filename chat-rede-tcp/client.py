"""
Exercício 3: Chat em Rede (TCP)
Cliente que se conecta ao servidor e permite envio e recebimento simultâneos.

Participante:
    - Daniel Gonçalves Lopes
"""

import socket
import threading
import sys

# Configurações de conexão
SERVER_HOST = '127.0.0.1'  # IP ou hostname do servidor
SERVER_PORT = 5001         # porta do chat
MAX_MSG = 1024             # tamanho máximo da mensagem em bytes

def receive_messages(sock):
    """
    Thread que fica em loop lendo do socket e imprimindo
    qualquer mensagem recebida do servidor.
    """
    while True:
        try:
            data = sock.recv(MAX_MSG)
            if not data:
                print('❌ Servidor desconectou.')
                break
            # imprime mensagem recebida e reposiciona prompt
            print('\n' + data.decode('utf-8') + '\n> ', end='')
        except:
            # encerra se ocorrer erro de leitura
            break

def main():
    """Conecta ao servidor, inicia thread de recebimento e loop de envio."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((SERVER_HOST, SERVER_PORT))
        except ConnectionRefusedError:
            print(f'❌ Não foi possível conectar a {SERVER_HOST}:{SERVER_PORT}')
            return

        # inicia thread emancipada para receber mensagens
        threading.Thread(
            target=receive_messages,
            args=(sock,),
            daemon=True
        ).start()

        print('🗨️ Conectado ao chat. Digite mensagens (ou "sair" para encerrar).')
        # loop principal de envio
        while True:
            msg = input('> ').strip()
            if not msg:
                continue  # ignora entrada vazia

            try:
                sock.sendall(msg.encode('utf-8'))
            except BrokenPipeError:
                # servidor fechou a conexão
                print('❌ Conexão encerrada.')
                break

            if msg.lower() == 'sair':
                # finaliza o cliente
                print('🔒 Você saiu do chat.')
                break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # encerra com Ctrl+C sem exibir traceback
        print('\n🔴 Cliente encerrado pelo usuário')
        sys.exit()
