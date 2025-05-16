#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercício 1: Cliente-Servidor TCP
Cliente que envia múltiplas mensagens válidas e recebe confirmações do servidor,
permanece ativo até o terminal ser fechado.

Participantes:
    - Daniel Gonçalves Lopes
    - Joana de Oliveira Rocha
    - João Victor Almeida
"""
import logging
from log_config import setup_logging
import socket
import sys

# Inicializa logging (arquivo e console)
setup_logging()
logger = logging.getLogger(__name__)

# Configurações de conexão
HOST = "127.0.0.1"  # endereço do servidor
PORT = 5000         # porta do servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção


def main():
    """
    Conecta ao servidor e, em loop, lê input do usuário, valida não vazio,
    envia mensagem e registra a resposta. Encerra apenas quando o terminal fechar.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                logger.info(f"Conectado a {HOST}:{PORT}")
            except ConnectionRefusedError:
                logger.error(f"Não foi possível conectar a {HOST}:{PORT}")
                return

            while True:
                try:
                    mensagem = input('✉️  Digite sua mensagem: ').strip()
                except (EOFError, KeyboardInterrupt):
                    logger.info('Terminal fechado. Encerrando cliente.')
                    break

                # ignora entrada vazia
                if not mensagem:
                    continue

                # envia dados ao servidor
                try:
                    s.sendall(mensagem.encode('utf-8'))
                    logger.info(f"Enviado: {mensagem}")
                except Exception as e:
                    logger.error(f"Erro ao enviar mensagem: {e}")
                    break

                # aguarda resposta
                try:
                    resposta = s.recv(BUFFER_SIZE).decode('utf-8')
                    if not resposta:
                        logger.warning('Conexão encerrada pelo servidor.')
                        break
                    logger.info(f"Resposta recebida: {resposta}")
                except Exception as e:
                    logger.error(f"Erro ao receber resposta: {e}")
                    break
    except Exception as e:
        logger.critical(f"Erro fatal no cliente TCP: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
