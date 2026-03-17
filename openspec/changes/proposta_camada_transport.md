# Camada Transport (Modo Teste)

## Contexto
Este documento especifica a versão simplificada da camada **transport**, voltada para testes de transmissão.  
Em vez de capturar e codificar em tempo real, o sistema utiliza um **vídeo já gravado** como fonte, reduzindo custo de processamento.

## Objetivos
- Validar a transmissão RTMP para YouTube Live sem sobrecarregar CPU/GPU.
- Usar vídeo pré-existente como entrada.
- Permitir configuração rápida de endpoint (URL + chave de stream).
- Garantir logs básicos de status da transmissão.

## Requisitos
- Compatibilidade com **FFmpeg** para envio de arquivo de vídeo.
- Suporte a formatos comuns (`.mp4`, `.webm`).
- Parâmetros leves de transmissão (bitrate reduzido, preset ultrafast).
- Reconexão simples em caso de falha.

## Estrutura Proposta


## Fluxo Simplificado
```mermaid
graph TD;
  video_file --> rtmp_test_transport_py;
  rtmp_test_transport_py --> YouTubeLive;