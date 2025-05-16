#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 1: Cliente-Servidor TCP
Servidor multithread que aceita conexões, valida mensagens e responde confirmação,
registrando eventos via logging.

Participantes:
    - Daniel Gonçalves Lopes
    - Joana de Oliveira Rocha
    - João Victor Almeida
"""
import logging
from log_config import setup_logging
import socket
import threading
import sys

# Inicializa logging (arquivo e console)
setup_logging()
logger = logging.getLogger(__name__)

# Configurações de rede
HOST = "0.0.0.0"  # escuta em todas as interfaces
PORT = 5000  # porta fixa para o serviço TCP
MAX_BUFFER = 1024  # tamanho do buffer para recepção de dados


def handle_client(conn, addr):
    """
    Lida com um cliente individual:
    - Recebe dados em loop
    - Valida mensagem não vazia
    - Registra logs de eventos e erros
    - Fecha conexão de forma segura
    """
    logger.info(f"Conexão recebida de {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(MAX_BUFFER)
                if not data:
                    logger.warning(f"Cliente {addr} desconectou.")
                    break

                message = data.decode("utf-8").strip()
                if not message:
                    erro = "Erro: mensagem vazia não é permitida"
                    conn.sendall(erro.encode("utf-8"))
                    logger.warning(f"Mensagem vazia recebida de {addr}")
                    continue

                logger.info(f"De {addr}: {message}")
                conn.sendall("Mensagem recebida".encode("utf-8"))
                logger.info(f"Confirmação enviada para {addr}")

            except ConnectionResetError:
                logger.error(f"Conexão perdida com {addr}")
                break
            except Exception as e:
                logger.error(f"Erro ao processar {addr}: {e}")
                break

    logger.info(f"Encerrada conexão com {addr}")


def main():
    """
    Inicializa o servidor TCP, aceita conexões e gerencia threads para cada cliente.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            logger.info(f"Servidor escutando em {HOST}:{PORT}...")

            while True:
                conn, addr = s.accept()
                thread = threading.Thread(
                    target=handle_client, args=(conn, addr), daemon=True
                )
                thread.start()
    except KeyboardInterrupt:
        logger.info("Servidor encerrado pelo usuário")
    except Exception as e:
        logger.critical(f"Erro fatal no servidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
