"""
Exercício 3: Chat em Rede (TCP)
Servidor que aceita 2 clientes e encaminha mensagens bidirecionais em tempo real.

Participante:
    - Daniel Gonçalves Lopes
"""

import socket
import threading

# Configurações de rede
HOST = '0.0.0.0'   # escuta em todas as interfaces
PORT = 5001       # porta do chat
MAX_MSG = 1024    # tamanho máximo da mensagem em bytes

def forward(src, dst, name_src, name_dst):
    """
    Encaminha tudo que chegar de `src` para `dst`.
    Recebe um nome para cada ponta para logs e saída no console.
    Se a mensagem for 'sair', notifica o outro cliente e encerra ambas conexões.
    """
    while True:
        try:
            data = src.recv(MAX_MSG)
            # se não vier nada, o cliente desconectou
            if not data:
                print(f'❌ {name_src} desconectou.')
                break

            msg = data.decode('utf-8').strip()  # decodifica e remove espaços extras

            # comando de saída
            if msg.lower() == 'sair':
                dst.sendall(f'**{name_src} saiu do chat**'.encode('utf-8'))
                print(f'⚠️  {name_src} solicitou saída.')
                break

            # encaminha mensagem devidamente formatada
            dst.sendall(f'{name_src}: {msg}'.encode('utf-8'))

        except ConnectionResetError:
            # cliente fechou abruptamente
            print(f'⚠️  Conexão perdida com {name_src}.')
            break
        except Exception as e:
            # trata qualquer outro erro
            print(f'❌ Erro no thread de {name_src}: {e}')
            break

    # tentativa de fechar ambos sockets (caso ainda estejam abertos)
    try: src.close()
    except: pass
    try: dst.close()
    except: pass

def main():
    """Inicializa o servidor, aceita dois clientes e dispara threads de encaminhamento."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT))
        server_sock.listen(2)  # só 2 clientes
        print(f'🔊 Servidor de chat rodando em {HOST}:{PORT}')
        print('⌛ Aguardando 2 clientes...')

        # aceita os dois clientes
        conn1, addr1 = server_sock.accept()
        print(f'✅ Cliente 1 conectado de {addr1}')
        conn1.sendall(
            'Você é o Cliente 1. Digite "sair" para encerrar.'.encode('utf-8')
        )

        conn2, addr2 = server_sock.accept()
        print(f'✅ Cliente 2 conectado de {addr2}')
        conn2.sendall(
            'Você é o Cliente 2. Digite "sair" para encerrar.'.encode('utf-8')
        )

        # threads que fazem o repasse de mensagens
        t1 = threading.Thread(
            target=forward,
            args=(conn1, conn2, 'Cliente1', 'Cliente2'),
            daemon=True
        )
        t2 = threading.Thread(
            target=forward,
            args=(conn2, conn1, 'Cliente2', 'Cliente1'),
            daemon=True
        )
        t1.start()
        t2.start()

        # aguarda o fim de ambas as threads para encerrar o servidor
        t1.join()
        t2.join()
        print('🔴 Chat encerrado.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # permite fechar com Ctrl+C sem stack trace
        print('\n🔴 Servidor encerrado pelo usuário')
