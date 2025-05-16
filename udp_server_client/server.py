#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 2: Echo UDP
Servidor que recebe datagramas e devolve o mesmo payload (eco), usando logging.

Participantes:
    - Daniel Gonçalves Lopes
    - Joana de Oliveira Rocha
    - João Victor Almeida
"""
import logging
from log_config import setup_logging
import socket

# Inicializa logging (arquivo e console)
setup_logging()
logger = logging.getLogger(__name__)

# Configurações de rede
HOST = "0.0.0.0"  # escuta em todas as interfaces
PORT = 6000  # porta fixa para o serviço de eco
MAX_MSG_SIZE = 65507  # payload máximo de UDP em IPv4 (65.507 bytes)


def main():
    """
    Cria socket UDP, vincula ao host/porta e entra em loop:
    - Recebe datagramas até MAX_MSG_SIZE+1 para detectar mensagens excessivas
    - Valida tamanho, registra log e envia de volta o payload recebido
    - Interrompe em KeyboardInterrupt
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        logger.info(f"Servidor UDP escutando em {HOST}:{PORT}...")

        while True:
            try:
                data, addr = sock.recvfrom(MAX_MSG_SIZE + 1)

                # valida tamanho máximo
                if len(data) > MAX_MSG_SIZE:
                    logger.warning(
                        f"Mensagem de {addr} excede {MAX_MSG_SIZE} bytes e foi ignorada."
                    )
                    continue

                message = data.decode("utf-8", errors="replace").strip()
                logger.info(f'Recebido de {addr}: "{message}"')

                # envia de volta exatamente o que foi recebido
                sock.sendto(data, addr)
                logger.info(f"Eco enviado para {addr}")

            except KeyboardInterrupt:
                logger.info("Servidor encerrado pelo usuário via KeyboardInterrupt")
                break
            except Exception as e:
                logger.error(f"Erro no servidor: {e}")


if __name__ == "__main__":
    main()
