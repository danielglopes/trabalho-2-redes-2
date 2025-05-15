"""
Exercício 2: Echo UDP
Cliente que envia datagramas e exibe o eco recebido.

Participante:
    - João Victor Almeida
"""

import socket

# Configurações de conexão
SERVER_HOST = '127.0.0.1'  # IP do servidor
SERVER_PORT = 6000         # mesma porta do servidor
MAX_MSG_SIZE = 65507       # payload máximo de UDP em IPv4
TIMEOUT = 2.0              # tempo limite em segundos


def main():
    """
    Cria socket UDP, seta timeout e entra em loop de envio:
    - Lê input do usuário até 'sair'
    - Valida tamanho de payload
    - Envia datagrama e aguarda eco
    - Trata timeout e erros de comunicação
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)
        print('✉️ Cliente UDP pronto. Digite mensagens (ou "sair" para encerrar).')

        while True:
            texto = input('> ').strip()
            if texto.lower() == 'sair':
                print('🔒 Encerrando cliente.')
                break

            payload = texto.encode('utf-8')
            # valida tamanho do datagrama
            if len(payload) > MAX_MSG_SIZE:
                print(f'⚠️ Erro: mensagem com {len(payload)} bytes excede o máximo de {MAX_MSG_SIZE}.')
                continue

            try:
                # envia para o servidor
                sock.sendto(payload, (SERVER_HOST, SERVER_PORT))
                # aguarda eco do servidor
                resp, addr = sock.recvfrom(MAX_MSG_SIZE)
                eco = resp.decode('utf-8', errors='replace')
                print(f'🔁 Eco recebido de {addr}: "{eco}"')

            except socket.timeout:
                print('⏱️ Tempo limite de resposta excedido (packet loss ou servidor fora).')
            except Exception as e:
                print(f'❌ Erro de comunicação: {e}')


if __name__ == '__main__':
    main()