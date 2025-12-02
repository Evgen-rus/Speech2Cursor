"""
Скрипт для массовой транскрибации уже готовых аудиофайлов.

Работает так:
- Показывает окно выбора файлов (можно выбрать сразу несколько аудио);
- Каждый файл по очереди отправляется в OpenAI для распознавания;
- Результат каждого файла сохраняется в отдельный .txt рядом с исходным аудио
  (как в одиночном скрипте file_transcribe.py).

Для транскрибации используется уже готовая асинхронная функция
`transcribe_file_async` из `file_transcribe.py`, чтобы не дублировать логику.
"""

import asyncio
from typing import List

from tkinter import Tk, filedialog, messagebox

from config import logger
from file_transcribe import transcribe_file_async, save_transcription


def choose_audio_files() -> list[str]:
    """
    Открывает диалог выбора нескольких файлов и возвращает список путей.

    Если пользователь ничего не выбрал — возвращает пустой список.
    """
    root = Tk()
    root.withdraw()
    root.update()  # Обновляем, чтобы окно диалога корректно появилось поверх

    filetypes = (
        ("Аудиофайлы", "*.wav *.mp3 *.ogg *.m4a *.flac *.webm"),
        ("Все файлы", "*.*"),
    )

    filepaths = filedialog.askopenfilenames(
        title="Выберите аудиофайлы для массовой транскрибации",
        filetypes=filetypes,
    )

    root.destroy()

    # `askopenfilenames` всегда возвращает кортеж, даже если ничего не выбрано.
    # Приводим к списку.
    return list(filepaths)


def transcribe_files_sequential(filepaths: List[str]) -> None:
    """
    Последовательно транскрибирует каждый файл в списке.

    Для каждого файла:
    - запускает `transcribe_file_async` через `asyncio.run`;
    - печатает прогресс в консоль;
    - сохраняет результат через `save_transcription`.
    """
    total = len(filepaths)
    success_count = 0
    error_count = 0

    for idx, filepath in enumerate(filepaths, start=1):
        print(f"\n=== Файл {idx}/{total} ===")
        print(f"Транскрибирую: {filepath}")
        logger.info(f"[batch] Начинаю транскрибацию файла {idx}/{total}: {filepath}")

        try:
            text = asyncio.run(transcribe_file_async(filepath))
        except Exception as e:  # noqa: BLE001 — здесь хотим поймать любую ошибку
            error_count += 1
            logger.error(f"[batch] Ошибка при транскрибации файла {filepath}: {e}")
            print(f"Ошибка при транскрибации этого файла: {e}")
            # Переходим к следующему файлу
            continue

        # Печатаем часть результата в консоль (полный текст — в .txt-файле)
        print("Распознанный текст (начало):")
        print("-" * 40)
        preview = text[:1000]  # первые 1000 символов, чтобы не засорять консоль
        print(preview)
        if len(text) > len(preview):
            print("... (остальной текст сохранён в файл)")
        print("-" * 40)

        # Сохраняем результат в текстовый файл
        txt_path = save_transcription(text, filepath)
        success_count += 1
        print(f"Транскрипция сохранена в файл:\n{txt_path}")

    # Итоговая сводка
    summary = (
        f"Обработано файлов: {total}\n"
        f"Успешно: {success_count}\n"
        f"С ошибками: {error_count}"
    )

    print("\n=== Массовая транскрибация завершена ===")
    print(summary)

    try:
        messagebox.showinfo("Массовая транскрибация завершена", summary)
    except Exception:
        # Если Tkinter по какой-то причине не смог показать окно — не критично.
        pass


def main() -> None:
    """
    Главная функция массовой транскрибации:
    1) Показывает окно выбора нескольких файлов;
    2) По очереди транскрибирует каждый файл;
    3) Сохраняет результат каждого файла в отдельный .txt.
    """
    print("=== Массовая транскрибация аудиофайлов (Speech2Cursor) ===")
    print("Сейчас откроется окно выбора ОДНОГО или НЕСКОЛЬКИХ файлов.")

    filepaths = choose_audio_files()
    if not filepaths:
        print("Файлы не выбраны. Выходим.")
        return

    print("\nВы выбрали следующие файлы для транскрибации:")
    for path in filepaths:
        print(f"- {path}")

    transcribe_files_sequential(filepaths)


if __name__ == "__main__":
    main()


