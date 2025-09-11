# Speech2Cursor

Project for recording voice from microphone and transcribing it to text using OpenAI API.

## Project Structure

- `audio_handler.py` - module for asynchronous voice message transcription
- `config.py` - project configuration (logging, environment variables)
- `mic_transcribe.py` - main script for recording from microphone and transcription
- `mic_transcribe_hotkey.py` - script with hotkey control (press Alt+S to record)
- `requirements.txt` - project dependencies
- `.env` - environment variables (API keys, settings)
- `.env.example` - example environment variables file

## System Requirements

- **Python 3.11** or higher
- Active internet connection
- Microphone for voice recording

## Installation

1. Make sure you have Python 3.11 or higher installed. Check version with:
   ```bash
   python --version
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/Evgen-rus/Speech2Cursor.git
   cd Speech2Cursor
   ```

3. Create virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Configure `.env` file:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and replace `OPENAI_API_KEY=Ваш API ключ OpenAI` with your real OpenAI API key.

## Usage

### Option 1: Standard Mode
Run the script:
```bash
python mic_transcribe.py
```

Recording Control:
- Press Enter to start recording
- Speak into the microphone
- Press Enter to stop recording
- Text is automatically copied to clipboard and ready to paste in chat with Ctrl+V

### Option 2: Hotkey Mode

#### Method 2.1: Command Line Launch
Run the script with hotkey control:
```bash
python mic_transcribe_hotkey.py
```

#### Method 2.2: Launch via .bat file (Windows)
For convenient Windows launch, you can use a .bat file:

1. Create a file `run_speech2cursor.bat` in the project root with the following content:
   ```batch
   @echo off
   echo Activating virtual environment...
   call venv\Scripts\activate.bat

   if %errorlevel% neq 0 (
       echo Virtual environment activation error!
       pause
       exit /b 1
   )

   echo Launching Speech2Cursor...
   python mic_transcribe_hotkey.py

   echo.
   echo Program completed.
   pause
   ```

2. Double-click the `run_speech2cursor.bat` file to launch

#### Method 2.3: Desktop Shortcut
Create a shortcut with the following target location:
```
[PROJECT_PATH]\venv\Scripts\python.exe [PROJECT_PATH]\mic_transcribe_hotkey.py
```

Where `[PROJECT_PATH]` is the full path to your Speech2Cursor project folder.

**Example for your path:**
```
C:\My_Scripts_PYTON\Speech2Cursor\venv\Scripts\python.exe C:\My_Scripts_PYTON\Speech2Cursor\mic_transcribe_hotkey.py
```

Hotkey Control:
- Press Alt+S to start recording
- Press Alt+S again to stop recording and start transcription
- Text is automatically copied to clipboard
- Press Ctrl+C to exit

## Troubleshooting

### Problem: "Microphone not found" or "No sound"
**Solution:**
1. Check that the microphone is connected and enabled
2. In Windows: Settings → Sound → Input
3. Make sure the microphone is selected as the default device
4. Restart your computer

### Problem: "Virtual environment activation error"
**Solution:**
1. Make sure virtual environment is created: `python -m venv venv`
2. In Windows use: `venv\Scripts\activate`
3. Check that Python is installed correctly

### Problem: "OpenAI API error" or "Invalid API key"
**Solution:**
1. Check API key in `.env` file
2. Make sure the key is active on OpenAI website
3. Check your OpenAI account balance
4. Ensure internet connection is available

### Problem: "Module not found" when running
**Solution:**
1. Activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. If problem persists: `pip install --upgrade -r requirements.txt`

### Problem: Hotkeys don't work
**Solution:**
1. Run the program as administrator
2. Check that other programs aren't intercepting Alt+S
3. Try different key combinations in the code

### Problem: Text not copied to clipboard
**Solution:**
1. Check that `pyperclip` is installed
2. Try running as administrator
3. On Linux/Mac may require additional setup

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
- `keyboard` - hotkey detection
- `python-dotenv` - environment variable loading

## Updating the Project

### Updating Dependencies
```bash
# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Upgrade all dependencies
pip install --upgrade -r requirements.txt
```

### Getting Latest Changes (if project is on GitHub)
```bash
git pull origin main
```

### Upgrading Python
If you want to use a newer Python version:
1. Download new Python from the official website
2. Create a new virtual environment
3. Reinstall dependencies

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
