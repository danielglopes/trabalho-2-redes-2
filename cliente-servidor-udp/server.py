"""
Exercício 2: Echo UDP
Servidor que recebe datagramas e devolve o mesmo payload (eco).

Participante:
    - João Victor Almeida
"""

import socket

# Configurações de rede
HOST = '0.0.0.0'      # escuta em todas as interfaces
PORT = 6000           # porta fixa para o serviço de eco
MAX_MSG_SIZE = 65507  # payload máximo de UDP em IPv4 (65.507 bytes)


def main():
    """
    Cria socket UDP, vincula ao host/porta e entra em loop:
    - Recebe datagramas até MAX_MSG_SIZE+1 para detectar mensagens excessivas
    - Valida tamanho, imprime no console e envia de volta o payload recebido
    - Interrompe em KeyboardInterrupt
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f'🔊 Servidor UDP escutando em {HOST}:{PORT}...')

        while True:
            try:
                # recebe dados e endereço de origem
                data, addr = sock.recvfrom(MAX_MSG_SIZE + 1)

                # valida tamanho máximo
                if len(data) > MAX_MSG_SIZE:
                    print(f'⚠️ Mensagem de {addr} excede {MAX_MSG_SIZE} bytes e foi ignorada.')
                    continue

                # decodifica com tolerância a erros e remove espaços
                message = data.decode('utf-8', errors='replace').strip()
                print(f'📨 Recebido de {addr}: "{message}"')

                # envia de volta exatamente o que foi recebido
                sock.sendto(data, addr)

            except KeyboardInterrupt:
                print('\n🔴 Servidor encerrado pelo usuário.')
                break
            except Exception as e:
                # log de erro genérico
                print(f'❌ Erro no servidor: {e}')


if __name__ == '__main__':
    main()