# Trabalho 2 – Redes de Computadores 2

Este repositório contém as soluções dos exercícios propostos na disciplina de Redes de Computadores 2 (Prof. Alessandro Vivas Andrade). Cada subdiretório implementa um exercício específico usando Python 3.10+ e demonstra conceitos de sockets, protocolos TCP/UDP e multithreading.

## 📂 Estrutura do Projeto.

## 🛠️ Requisitos

* Python 3.10 ou superior
* (Opcional) Docker e Docker Compose, se desejar executar em contêineres

## 🚀 Como Executar (Modo Local)

Para cada exercício, abra um terminal, entre no respectivo diretório e execute:

### Exercício 1 – Cliente-Servidor TCP

```bash
cd cliente-servidor-tcp
# No terminal A (servidor)
python3 server.py
# No terminal B (cliente)
python3 client.py
```

### Exercício 2 – Echo UDP

```bash
cd cliente-servidor-udp
# No terminal A (servidor)
python3 server.py
# No terminal B (cliente)
python3 client.py
```

### Exercício 3 – Chat Rede TCP

```bash
cd chat-rede-tcp
# No terminal A (servidor)
python3 server.py
# No terminal B e C (clientes)
python3 client.py
```

### Exercício 4 – Servidor de Horas

```bash
cd servidor-horas
# No terminal A (servidor)
python3 server.py
# No terminal B (cliente)
python3 client.py
```

## 🐳 Docker

Caso queira usar Docker e Docker Compose, siga estas etapas na raiz do projeto:

1. **Build da imagem**

   ```bash
   docker-compose build
   ```
2. **Executar apenas o servidor e o cliente interativo**

   ```bash
   # Subir servidor em backgound
   docker-compose up -d ex1-tcp-server

   # Executar cliente interativo (conecta stdin/stdout)
   docker-compose run --rm ex1-tcp-client
   ```
3. **Parar e remover containers**

   ```bash
   docker-compose down
   ```

> No modo `host` (Linux), os containers compartilham a rede do host, permitindo que `127.0.0.1:<porta>` funcione corretamente.

## 📄 Descrição dos Exercícios

1. **cliente-servidor-tcp**: troca de mensagens simples via TCP com confirmação e validação de entrada.
2. **cliente-servidor-udp**: serviço de eco via UDP, tratamento de timeouts e tamanho máximo de datagrama.
3. **chat-rede-tcp**: chat bidirecional entre dois clientes, usando threads para envio e recepção paralelos.
4. **servidor-horas**: servidor multithread que retorna a hora atual (`HH:MM:SS`) e registra logs de requisição.

## 👥 Participantes

- Daniel Gonçalves Lopes
- Joana de Oliveira Rocha
- João Victor Almeida

## 📜 Licença

Trabalho acadêmico desenvolvido para a disciplina de Redes de Computadores 2. Uso restrito a fins de estudo.
