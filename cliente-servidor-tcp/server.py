"""
Exercício 1: Cliente-Servidor TCP
Servidor multithread que aceita conexões, valida mensagens e responde confirmação.

Participantes:
    - Daniel Gonçalves Lopes
    - Joana de Oliveira Rocha
    - João Victor Almeida
"""

import socket
import threading

# Configurações de rede
HOST = '0.0.0.0'      # escuta em todas as interfaces
PORT = 5000           # porta fixa para o serviço TCP
MAX_BUFFER = 1024     # tamanho do buffer para recepção de dados


def handle_client(conn, addr):
    """
    Lida com um cliente individual:
    - Recebe dados em loop
    - Valida mensagem não vazia
    - Imprime no console e envia confirmação de recebimento
    - Fecha conexão de forma segura
    """
    print(f'▶ Conexão recebida de {addr}')
    with conn:
        while True:
            try:
                data = conn.recv(MAX_BUFFER)
                # se recv retornar bytes vazios, cliente desconectou
                if not data:
                    print(f'⏹ Cliente {addr} desconectou.')
                    break

                message = data.decode('utf-8').strip()
                # validação de mensagem vazia
                if not message:
                    erro = 'Erro: mensagem vazia não é permitida'
                    conn.sendall(erro.encode('utf-8'))
                    continue

                # imprime a mensagem recebida no servidor
                print(f'📨 De {addr}: {message}')
                # envia confirmação ao cliente
                conn.sendall('Mensagem recebida'.encode('utf-8'))

            except ConnectionResetError:
                # cliente fechou abruptamente
                print(f'⚠️ Conexão perdida com {addr}')
                break
            except Exception as e:
                # log de erro genérico
                print(f'❌ Erro ao processar {addr}: {e}')
                break

    # fim do with conn: socket fechado automaticamente
    print(f'❌ Encerrada conexão com {addr}')


def main():
    """
    Inicializa o servidor TCP e gerencia threads para cada cliente.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # permite reusar o endereço rapidamente
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f'🔊 Servidor escutando em {HOST}:{PORT}...')

        while True:
            try:
                conn, addr = s.accept()
                # dispara nova thread para cada cliente
                thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()
            except KeyboardInterrupt:
                # permite parar o servidor com Ctrl+C
                print('\n🔴 Servidor encerrado pelo usuário')
                break
            except Exception as e:
                print(f'❌ Erro no servidor: {e}')
                continue


if __name__ == '__main__':
    main()