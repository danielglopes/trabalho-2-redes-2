"""
Exercício 4: Servidor de Hora Multithread TCP
Servidor que retorna a hora atual formatada ao receber requisição.

Participante:
    - João Victor Almeida
"""

import socket
import threading
import logging
from datetime import datetime

# Configurações de rede
HOST = '0.0.0.0'   # escuta em todas as interfaces
PORT = 7000        # porta fixa para o serviço de hora
ENCODING = 'utf-8'
BUFFER_SIZE = 1024

# Configuração do logger para registrar logs de solicitação e resposta
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def handle_client(conn, addr):
    """
    Lê a requisição do cliente, registra log e envia a hora atual no formato HH:MM:SS.
    """
    logging.info(f'Conexão iniciada por {addr}')
    try:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            logging.warning(f'{addr} enviou payload vazio. Encerrando.')
            return

        logging.info(f'Requisição recebida de {addr}: {data.decode(ENCODING)!r}')

        # Gera a hora atual formatada
        now = datetime.now().strftime('%H:%M:%S')
        conn.sendall(now.encode(ENCODING))
        logging.info(f'Enviado horário {now} para {addr}')

    except Exception as e:
        logging.error(f'Erro ao atender {addr}: {e}')
    finally:
        conn.close()
        logging.info(f'Conexão encerrada com {addr}')


def main():
    """
    Inicializa o servidor TCP, aceita conexões e cria threads para cada cliente.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        logging.info(f'Servidor de hora rodando em {HOST}:{PORT} …')

        while True:
            try:
                conn, addr = server_sock.accept()
                # Cria uma thread daemon para cada cliente
                t = threading.Thread(
                    target=handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                t.start()
            except KeyboardInterrupt:
                logging.info('Servidor encerrado pelo usuário (KeyboardInterrupt)')
                break
            except Exception as e:
                logging.error(f'Erro no loop principal: {e}')

if __name__ == '__main__':
    main()