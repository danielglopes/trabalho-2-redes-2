#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 3: Chat em Rede (TCP)
Servidor que aceita 2 clientes e encaminha mensagens bidirecionais em tempo real, usando logging.

Participantes:
    - Daniel Gonçalves Lopes
    - Joana de Oliveira Rocha
    - João Victor Almeida
"""
import logging
from log_config import setup_logging

# Inicializa logging para console e arquivo
setup_logging()
logger = logging.getLogger(__name__)

import socket
import threading

# Configurações de rede
HOST = "0.0.0.0"  # escuta em todas as interfaces
PORT = 5001  # porta do chat
MAX_MSG = 1024  # tamanho máximo da mensagem em bytes


def forward(src, dst, name_src, name_dst):
    """
    Encaminha mensagens de src para dst.
    Usa logger para registrar eventos.
    """
    while True:
        try:
            data = src.recv(MAX_MSG)
            if not data:
                logger.warning(f"{name_src} desconectou.")
                break

            msg = data.decode("utf-8").strip()
            if msg.lower() == "sair":
                dst.sendall(f"**{name_src} saiu do chat**".encode("utf-8"))
                logger.info(f"{name_src} solicitou saída.")
                break

            dst.sendall(f"{name_src}: {msg}".encode("utf-8"))
            logger.info(f"Mensagem de {name_src} para {name_dst}: {msg}")

        except ConnectionResetError:
            logger.error(f"Conexão perdida com {name_src}.")
            break
        except Exception as e:
            logger.error(f"Erro no thread de {name_src}: {e}")
            break

    # Encerra ambos sockets
    try:
        src.close()
    except Exception:
        pass
    try:
        dst.close()
    except Exception:
        pass


def main():
    """
    Inicializa o servidor, aceita dois clientes e dispara threads de encaminhamento.
    Registra status e erros com logger.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen(2)
        logger.info(f"Servidor de chat rodando em {HOST}:{PORT}")
        logger.info("Aguardando 2 clientes...")

        conn1, addr1 = server_sock.accept()
        logger.info(f"Cliente 1 conectado de {addr1}")
        conn1.sendall(
            'Você é o Cliente 1. Digite "sair" para encerrar.'.encode("utf-8")
        )

        conn2, addr2 = server_sock.accept()
        logger.info(f"Cliente 2 conectado de {addr2}")
        conn2.sendall(
            'Você é o Cliente 2. Digite "sair" para encerrar.'.encode("utf-8")
        )

        t1 = threading.Thread(
            target=forward, args=(conn1, conn2, "Cliente1", "Cliente2"), daemon=True
        )
        t2 = threading.Thread(
            target=forward, args=(conn2, conn1, "Cliente2", "Cliente1"), daemon=True
        )
        t1.start()
        t2.start()

        t1.join()
        t2.join()
        logger.info("Chat encerrado.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Servidor encerrado pelo usuário")
