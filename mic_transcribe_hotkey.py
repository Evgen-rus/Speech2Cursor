import asyncio
import io
import threading
import time
from typing import List, Optional

import keyboard
import numpy as np
import sounddevice as sd
import soundfile as sf
import pyperclip

from audio_handler import transcribe_voice
from config import logger


class VoiceRecorder:
    """Класс для записи голоса с управлением горячими клавишами."""

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.recorded_chunks: List[np.ndarray] = []
        self.stream: Optional[sd.InputStream] = None

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback для обработки аудио-потока."""
        if status:
            logger.warning(f"Статус аудиопотока: {status}")
        if self.is_recording:
            self.recorded_chunks.append(indata.copy())

    def start_recording(self):
        """Начать запись."""
        if not self.is_recording:
            self.is_recording = True
            self.recorded_chunks = []
            logger.info("Запись начата")
            print("🎤 Запись... (нажмите Alt+S для остановки)")

    def stop_recording(self) -> Optional[bytes]:
        """Остановить запись и вернуть WAV-байты."""
        if self.is_recording:
            self.is_recording = False
            logger.info("Запись остановлена")

            if not self.recorded_chunks:
                print("❌ Ничего не записано")
                return None

            # Формируем WAV
            audio_data = np.concatenate(self.recorded_chunks, axis=0)
            buffer = io.BytesIO()
            sf.write(buffer, audio_data, self.sample_rate, format="WAV", subtype="PCM_16")
            buffer.seek(0)
            return buffer.read()

        return None

    def run(self):
        """Запуск основного цикла."""
        print("🎙️ Speech2Cursor Hotkey Mode")
        print("Нажмите Alt+S для начала/остановки записи")
        print("Для выхода нажмите Ctrl+C или закройте окно")
        print("-" * 50)

        def on_alt_s_press():
            """Обработчик нажатия Alt+S."""
            if not self.is_recording:
                self.start_recording()
            else:
                # Если уже записываем - останавливаем
                wav_bytes = self.stop_recording()
                if wav_bytes:
                    # Запускаем транскрибацию в отдельном потоке
                    threading.Thread(target=self._transcribe_async, args=(wav_bytes,)).start()

        # Устанавливаем обработчик только для нажатия
        keyboard.add_hotkey('alt+s', on_alt_s_press, suppress=True)

        # Запускаем аудио-поток
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            callback=self._audio_callback
        ):
            try:
                keyboard.wait()  # Ждем событий клавиатуры
            except KeyboardInterrupt:
                print("\n👋 Выход из программы...")
            finally:
                keyboard.clear_all_hotkeys()

    def _transcribe_async(self, wav_bytes: bytes):
        """Асинхронная транскрибация в отдельном потоке."""
        async def transcribe():
            try:
                print("⏳ Обрабатываю...")
                text = await transcribe_voice(wav_bytes, file_name="voice.wav", language="ru")

                print("\n📝 Распознанный текст:")
                print("─" * 40)
                print(text)
                print("─" * 40)

                try:
                    pyperclip.copy(text)
                    print("✅ Скопировано в буфер обмена (Ctrl+V)")
                except Exception as clip_err:
                    logger.warning(f"Не удалось скопировать в буфер обмена: {clip_err}")

                print("\n🎙️ Готово! Нажмите Alt+S для новой записи\n")

            except Exception as e:
                logger.error(f"Ошибка транскрибации: {e}")
                print(f"❌ Ошибка транскрибации: {e}")

        # Запускаем асинхронную задачу
        asyncio.run(transcribe())


def main():
    """Главная функция."""
    recorder = VoiceRecorder()
    recorder.run()


if __name__ == "__main__":
    main()
