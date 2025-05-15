# Participantes:
# - Daniel Gonçalves Lopes
# - Joana de Oliveira Rocha
# - João Victor Almeida
FROM python:3.13-alpine

# Diretório de trabalho dentro do container
WORKDIR /app

# Copia todo o projeto para /app
COPY . /app

# Instala bash para acessos interativos (opcional)
RUN apk update && apk add bash

# Expor portas (informativo apenas)
EXPOSE 5000 5001 6000/udp 7000

# Comando padrão ao iniciar o container
CMD ["bash"]