# Screen Streamer

> Transmissor de tela para YouTube e outras plataformas, com captura, compressão, gravação e transmissão de vídeo.

## Funcionalidades
- Captura de tela em tempo real
- Compressão de frames usando JPEG
- Gravação de vídeo com áudio via FFmpeg
- Interface gráfica simples (Tkinter)
- Suporte a transmissão e integração futura com redes

## Estrutura do Projeto

- `main.py`: Exemplo de uso da captura e compressão de tela
- `capture/`: Módulo de captura de tela
- `encoder/`: Módulo de compressão de frames
- `recorder/`: Gravação de vídeo com FFmpeg
- `ui/`: Interface gráfica para gravação
- `test/`: Scripts de teste

## Requisitos

- Python 3.8+
- FFmpeg instalado e disponível no PATH do sistema
- Sistema operacional: Windows (suporte principal)

## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/SoftwMicro/screen_streamer.git
   cd screen-streamer
   ```
2. Crie um ambiente virtual (opcional, mas recomendado):
   ```sh
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Instale o FFmpeg:
   - Baixe em: https://ffmpeg.org/download.html
   - Adicione o executável ao PATH do sistema

## Dependências

As principais dependências estão em `requirements.txt`:

- mss
- opencv-python
- ffmpeg-python
- websockets
- PyYAML
- numpy
- pyautogui
- tkinter (já incluído no Python para Windows)

## Como usar

- Para capturar e comprimir frames:
  ```sh
  python main.py
  ```
- Para abrir a interface gráfica de gravação:
  ```sh
  python ui/app.py
  ```
- Para rodar testes:
  ```sh
  python test/ffmpeg_screen_capture_example.py
  ```

## Observações
- O FFmpeg deve estar corretamente instalado e acessível pelo terminal.
- O projeto está em desenvolvimento e novas funcionalidades podem ser adicionadas.

## Licença

MIT
