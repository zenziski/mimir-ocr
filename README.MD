# Nome do Projeto

Este é um guia rápido para começar a trabalhar neste projeto.

## Pré-requisitos

Este projeto é executado usando Docker Compose. Se você ainda não tem o Docker e o Docker Compose instalados, siga as instruções de instalação na documentação oficial do Docker:

- [Instalação do Docker](https://docs.docker.com/get-docker/)
- [Instalação do Docker Compose](https://docs.docker.com/compose/install/)

## Como executar o projeto

Para executar este projeto, siga estas etapas:

1. Clone o repositório do projeto.
2. Navegue até o diretório do projeto.
3. Crie um arquivo chamado `docker-compose.yml` com o seguinte conteúdo:

```yml
version: '3'

services:
  mimir:
    build: .
    ports:
      - "80:5000"
    expose:
      - "5000"
    command: python3 server.py
```

4. Execute o comando `docker-compose build`. Este comando constrói os serviços do projeto.
5. Após a construção bem-sucedida, execute o comando `docker-compose up`. Este comando inicia os serviços do projeto.
6. Quando terminar de usar os serviços, você pode pará-los com o comando `docker-compose down`.

## Sobre as funções de pré-processamento e leitura de dados

Este projeto inclui funções para pré-processar imagens e ler dados de texto fornecidos por um OCR.

A função de pré-processamento recebe um caminho de imagem como entrada. Ele carrega a imagem, converte-a para escala de cinza, aplica dilatação e erosão para remover ruídos, aplica um limite adaptativo para obter uma imagem binária e, finalmente, salva a imagem processada.

A função de leitura de dados recebe um texto como entrada. Ele usa expressões regulares para encontrar e extrair informações específicas do texto. As expressões regulares podem ser personalizadas para extrair diferentes tipos de informações.

Por favor, consulte o código e os comentários para mais detalhes sobre como essas funções funcionam.