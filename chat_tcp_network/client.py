#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 3: Chat em Rede (TCP)
Cliente que se conecta ao servidor e permite envio e recebimento simultâneos, usando logging.

Participantes:
    - Daniel Gonçalves Lopes
    - Joana de Oliveira Rocha
    - João Victor Almeida
"""
import logging
from log_config import setup_logging

# Inicializa logging (arquivo e console)
setup_logging()
logger = logging.getLogger(__name__)

import socket
import threading
import sys

# Configurações de conexão
SERVER_HOST = "127.0.0.1"  # IP ou hostname do servidor
SERVER_PORT = 5001  # porta do chat
MAX_MSG = 1024  # tamanho máximo da mensagem em bytes


def receive_messages(sock):
    """
        Thread que fica em loop lendo do socket e registrando
    eas mensagens recebidas.
    """
    while True:
        try:
            data = sock.recv(MAX_MSG)
            if not data:
                logger.error("Servidor desconectou.")
                break
            # loga mensagem recebida
            logger.info(data.decode("utf-8"))
        except Exception:
            break


def main():
    """
    Conecta ao servidor, inicia thread de recebimento e loop de envio,
    registrando eventos via logger.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((SERVER_HOST, SERVER_PORT))
        except ConnectionRefusedError:
            logger.error(f"Não foi possível conectar a {SERVER_HOST}:{SERVER_PORT}")
            return

        # inicia thread para receber mensagens do servidor
        threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

        logger.info('Conectado ao chat. Digite mensagens (ou "sair" para encerrar).')
        while True:
            msg = input("> ").strip()
            if not msg:
                continue  # ignora entrada vazia

            try:
                sock.sendall(msg.encode("utf-8"))
            except BrokenPipeError:
                logger.error("Conexão encerrada.")
                break

            if msg.lower() == "sair":
                logger.info("Você saiu do chat.")
                break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Cliente encerrado pelo usuário")
        sys.exit()
