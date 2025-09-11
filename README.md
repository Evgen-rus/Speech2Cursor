# Speech2Cursor

Project for recording voice from microphone and transcribing it to text using OpenAI API.

## Project Structure

- `audio_handler.py` - module for asynchronous voice message transcription
- `config.py` - project configuration (logging, environment variables)
- `mic_transcribe.py` - main script for recording from microphone and transcription
- `requirements.txt` - project dependencies
- `.env` - environment variables (API keys, settings)
- `.env.example` - example environment variables file

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Evgen-rus/Speech2Cursor.git
   cd Speech2Cursor
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure `.env` file:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and replace `OPENAI_API_KEY=Ваш API ключ OpenAI` with your real OpenAI API key.

## Usage

Run the script:
```bash
python mic_transcribe.py
```

### Recording Control:
- Press Enter to start recording
- Speak into the microphone
- Press Enter to stop recording
- Text is automatically copied to clipboard and ready to paste in chat with Ctrl+V

### Repeat:
- Enter - repeat recording
- n - exit

## Limitations

The project was originally created for convenient work in Cursor — short voice messages for fast transcription.

- Maximum recording length: ~12-13 minutes (API limit ~25 MB)
- Recommended length: 1-5 minutes for optimal speed
- Requires active internet connection for transcription
- Recording format: WAV (16 kHz, 16-bit, mono)

## Dependencies

- `openai` - API for transcription
- `sounddevice` - microphone recording
- `soundfile` - audio file handling
- `numpy` - audio data processing
- `pyperclip` - clipboard copying
- `python-dotenv` - environment variable loading
