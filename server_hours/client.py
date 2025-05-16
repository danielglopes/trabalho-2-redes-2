#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 4: Cliente de Hora TCP
Cliente que solicita a hora ao servidor e exibe no console, usando logging.

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
import sys

# Configurações de conexão
SERVER_HOST = "127.0.0.1"  # endereço do servidor
SERVER_PORT = 7000  # mesma porta do servidor
ENCODING = "utf-8"
BUFFER_SIZE = 1024


def main():
    """
    Conecta ao servidor, envia requisição GET_TIME e registra a hora recebida.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((SERVER_HOST, SERVER_PORT))
            logger.info(f"Conectado a {SERVER_HOST}:{SERVER_PORT}")
        except ConnectionRefusedError:
            logger.error(f"Não foi possível conectar a {SERVER_HOST}:{SERVER_PORT}")
            sys.exit(1)

        # Envia comando para solicitar horário
        req = "GET_TIME"
        sock.sendall(req.encode(ENCODING))
        logger.info(f"Enviado requisição: {req}")

        # Aguarda resposta do servidor
        try:
            data = sock.recv(BUFFER_SIZE)
        except Exception as e:
            logger.error(f"Erro ao receber dados: {e}")
            sys.exit(1)

        if not data:
            logger.error("Servidor não enviou dados.")
            sys.exit(1)

        hora = data.decode(ENCODING)
        logger.info(f"Hora atual recebida: {hora}")


if __name__ == "__main__":
    main()
