#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 2: Echo UDP
Cliente que envia datagramas e exibe o eco recebido, usando logging.

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
SERVER_HOST = "127.0.0.1"  # IP do servidor
SERVER_PORT = 6000  # mesma porta do servidor
MAX_MSG_SIZE = 65507  # payload máximo de UDP em IPv4
TIMEOUT = 2.0  # tempo limite em segundos


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
        logger.info('Cliente UDP pronto. Digite mensagens (ou "sair" para encerrar).')

        while True:
            texto = input("> ").strip()
            if texto.lower() == "sair":
                logger.info("Encerrando cliente.")
                break

            payload = texto.encode("utf-8")
            if len(payload) > MAX_MSG_SIZE:
                logger.warning(
                    f"Mensagem com {len(payload)} bytes excede o máximo de {MAX_MSG_SIZE}."
                )
                continue

            try:
                sock.sendto(payload, (SERVER_HOST, SERVER_PORT))
                logger.info(f"Enviado para {SERVER_HOST}:{SERVER_PORT} -> {texto}")

                resp, addr = sock.recvfrom(MAX_MSG_SIZE)
                eco = resp.decode("utf-8", errors="replace")
                logger.info(f'Eco recebido de {addr}: "{eco}"')

            except socket.timeout:
                logger.error(
                    "Tempo limite de resposta excedido (packet loss ou servidor fora)."
                )
            except Exception as e:
                logger.error(f"Erro de comunicação: {e}")


if __name__ == "__main__":
    main()
