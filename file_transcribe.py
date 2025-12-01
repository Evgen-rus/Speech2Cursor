"""
Отдельный скрипт для транскрибации уже готового аудиофайла.

При запуске открывается окно выбора файла, затем файл отправляется
в OpenAI для распознавания, а результат сохраняется в .txt с датой и временем.
"""

import asyncio
import os
from datetime import datetime

from tkinter import Tk, filedialog, messagebox

from audio_handler import transcribe_voice
from config import logger


def choose_audio_file() -> str | None:
    """
    Открывает диалог выбора файла и возвращает путь к выбранному файлу
    или None, если пользователь ничего не выбрал.
    """
    # Создаём скрытое главное окно Tkinter только для диалога выбора файла
    root = Tk()
    root.withdraw()
    root.update()  # Обновляем, чтобы окно диалога корректно появилось поверх

    filetypes = (
        ("Аудиофайлы", "*.wav *.mp3 *.ogg *.m4a *.flac *.webm"),
        ("Все файлы", "*.*"),
    )

    filepath = filedialog.askopenfilename(
        title="Выберите аудиофайл для транскрибации",
        filetypes=filetypes,
    )

    root.destroy()

    # Если пользователь нажал «Отмена», вернём None
    return filepath or None


async def transcribe_file_async(filepath: str) -> str:
    """
    Асинхронно читает аудиофайл и отправляет его в transcribe_voice.
    """
    logger.info(f"Открываю файл для транскрибации: {filepath}")

    # Читаем файл в память как байты
    with open(filepath, "rb") as f:
        voice_data = f.read()

    if not voice_data:
        raise ValueError("Файл пустой или не удалось прочитать данные")

    file_name = os.path.basename(filepath)

    # Используем уже существующую функцию транскрибации
    text = await transcribe_voice(voice_data, file_name=file_name, language="ru")
    return text


def save_transcription(text: str, original_filepath: str) -> str:
    """
    Сохраняет транскрибацию в .txt-файл рядом с исходным аудио.

    Имя файла: <имя_аудио>_transcription_YYYY-MM-DD_HH-MM-SS.txt
    Возвращает путь к созданному файлу.
    """
    base_dir = os.path.dirname(original_filepath)
    base_name = os.path.splitext(os.path.basename(original_filepath))[0]

    # Дата и время в имени файла, чтобы файлы не перезаписывались
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    txt_name = f"{base_name}_transcription_{timestamp}.txt"
    txt_path = os.path.join(base_dir, txt_name)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    logger.info(f"Транскрипция сохранена в файл: {txt_path}")
    return txt_path


def main() -> None:
    """
    Главная функция:
    1) Показывает окно выбора файла
    2) Отправляет файл в транскрибацию
    3) Сохраняет результат в .txt
    """
    print("=== Транскрибация аудиофайла (Speech2Cursor) ===")
    print("Сейчас откроется окно выбора файла.")

    filepath = choose_audio_file()
    if not filepath:
        print("Файл не выбран. Выходим.")
        return

    print(f"Вы выбрали файл: {filepath}")

    try:
        # Запускаем асинхронную транскрибацию в синхронном скрипте
        text = asyncio.run(transcribe_file_async(filepath))
    except Exception as e:
        logger.error(f"Ошибка при транскрибации файла: {e}")
        # Покажем также всплывающее окно, чтобы было нагляднее
        try:
            messagebox.showerror("Ошибка транскрибации", str(e))
        except Exception:
            # Если Tkinter по какой-то причине не может показать сообщение,
            # просто игнорируем это и остаёмся в консоли.
            pass
        print(f"Ошибка транскрибации: {e}")
        return

    print("\nРаспознанный текст:")
    print("-" * 40)
    print(text)
    print("-" * 40)

    # Сохраняем результат в текстовый файл
    txt_path = save_transcription(text, filepath)
    print(f"\nТранскрипция сохранена в файл:\n{txt_path}")

    # Небольшое окно-подтверждение (если запущено из проводника, чтобы было видно результат)
    try:
        messagebox.showinfo("Готово", f"Текст сохранён в файл:\n{txt_path}")
    except Exception:
        pass


if __name__ == "__main__":
    main()


