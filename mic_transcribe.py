import asyncio
import io
from typing import List

import numpy as np
import sounddevice as sd
import soundfile as sf

from audio_handler import transcribe_voice
from config import logger


def record_audio(sample_rate: int = 16000, channels: int = 1) -> bytes:
    """
    Записывает звук с микрофона до нажатия Enter и возвращает WAV-байты (PCM 16 бит).
    """
    recorded_chunks: List[np.ndarray] = []

    def _callback(indata, frames, time_info, status):
        if status:
            logger.warning(f"Статус аудиопотока: {status}")
        recorded_chunks.append(indata.copy())

    input("Нажмите Enter для начала записи...")
    logger.info("Запись начата. Говорите...")
    with sd.InputStream(samplerate=sample_rate, channels=channels, dtype="int16", callback=_callback):
        input("Запись... нажмите Enter для остановки")

    logger.info("Запись остановлена. Формирую WAV...")
    if not recorded_chunks:
        return b""

    audio_data = np.concatenate(recorded_chunks, axis=0)
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sample_rate, format="WAV", subtype="PCM_16")
    buffer.seek(0)
    return buffer.read()


async def main() -> None:
    while True:
        wav_bytes = record_audio(sample_rate=16000, channels=1)
        if not wav_bytes:
            print("Ничего не записано. Повторим.")
            continue

        try:
            text = await transcribe_voice(wav_bytes, file_name="voice.wav", language="ru")
            print("\nРаспознанный текст:")
            print("--------------------------------")
            print(text)
            print("--------------------------------\n")
        except Exception as e:
            logger.error(f"Ошибка транскрибации: {e}")

        choice = input("Ещё раз? [Enter - да / n - выход]: ").strip().lower()
        if choice == "n":
            break


if __name__ == "__main__":
    asyncio.run(main())


