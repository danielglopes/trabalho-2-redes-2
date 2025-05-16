# Trabalho 2 – Redes de Computadores 2

Este repositório contém as soluções dos exercícios propostos na disciplina de Redes de Computadores 2 (Prof. Alessandro Vivas Andrade). Cada subdiretório implementa um exercício específico usando Python 3.10+ e demonstra conceitos de sockets, protocolos TCP/UDP e multithreading.

## 📂 Estrutura do Projeto

```
.
├── chat_tcp_network/        # Exercício 3: Chat TCP
│   ├── client.py
│   └── server.py
│
├── tcp_server_client/       # Exercício 1: Cliente-Servidor TCP
│   ├── client.py
│   └── server.py
│
├── udp_server_client/       # Exercício 2: Echo UDP
│   ├── client.py
│   └── server.py
│
├── server_hours/            # Exercício 4: Servidor de Horas
│   ├── client.py
│   └── server.py
│
├── log_config.py            # Configuração global de logging
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
└── logs/                    # Arquivos de log gerados
```

## 🛠️ Requisitos

- Python 3.10 ou superior
- (Opcional) Docker e Docker Compose, para execução em contêineres

## 🚀 Como Executar (Modo Local)

Execute cada exercício diretamente do **diretório raiz** usando o parâmetro `-m`:

### Exercício 1 – Cliente-Servidor TCP

```bash
# Terminal A (servidor)
python3 -m tcp_server_client.server

# Terminal B (cliente)
python3 -m tcp_server_client.client
```

### Exercício 2 – Echo UDP

```bash
# Terminal A (servidor)
python3 -m udp_server_client.server

# Terminal B (cliente)
python3 -m udp_server_client.client
```

### Exercício 3 – Chat TCP

```bash
# Terminal A (servidor)
python3 -m chat_tcp_network.server

# Terminal B e C (clientes)
python3 -m chat_tcp_network.client
```

### Exercício 4 – Servidor de Horas

```bash
# Terminal A (servidor)
python3 -m server_hours.server

# Terminal B (cliente)
python3 -m server_hours.client
```

## 🐳 Docker

Para execução com Docker e Docker Compose, na raiz do projeto:

1. **Build da imagem**
   ```bash
   docker compose build
   ```
2. **Executar servidor e cliente interativos**
   ```bash
   # Exemplo para Exercício 1
   docker compose up -d tcp-server
   docker compose run --rm tcp-client
   ```
3. **Parar e remover containers**
   ```bash
   docker compose down
   ```

> No modo `host` (Linux), os containers compartilham a rede do host, permitindo que `127.0.0.1:<porta>` funcione corretamente.

## 📄 Descrição dos Exercícios

1. **tcp_server_client**: troca de mensagens simples via TCP com confirmação e validação de entrada.
2. **udp_server_client**: serviço de eco via UDP, tratamento de timeouts e tamanho máximo de datagrama.
3. **chat_tcp_network**: chat bidirecional entre dois clientes, usando threads para envio e recepção paralelos.
4. **server_hours**: servidor multithread que retorna a hora atual (`HH:MM:SS`) e registra logs de requisição.

## 👥 Participantes

- Daniel Gonçalves Lopes
- Joana de Oliveira Rocha
- João Victor Almeida

## 📜 Licença

Trabalho acadêmico desenvolvido para a disciplina de Redes de Computadores 2. Uso restrito a fins de estudo.
