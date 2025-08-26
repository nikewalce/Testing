import random
import re
from pathlib import Path

# Паттерн для поиска пустых @ExternalId
EMPTY_EXTERNAL_ID_PATTERN = re.compile(r"@ExternalId=\s*(?=\s|$)")
# Паттерн для поиска уже существующих ExternalId с пятизначными значениями
EXISTING_EXTERNAL_ID_PATTERN = re.compile(r"@ExternalId=(\d{5})")


def generate_unique_five_digit_id(existing_ids):
    """
    Генерирует уникальный пятизначный идентификатор
    :param existing_ids: Множество имеющихся идентификаторов в фича файлах.
    """
    while True:
        new_id = str(random.randint(1000000000, 9999999999))
        if new_id not in existing_ids:
            return new_id


def extract_existing_ids(content, existing_ids):
    """
    Находит все существующие пятизначные идентификаторы @ExternalId и добавляет их в множество.
    :param content: Содержимое файла, представленное в виде строки.
    :param existing_ids: Множество, в которое будут добавлены существующие идентификаторы
    """
    matches = EXISTING_EXTERNAL_ID_PATTERN.findall(content)
    existing_ids.update(matches)


def replace_empty_external_ids(content, existing_ids):
    """
    Заменяет пустые @ExternalId на уникальные значения.
    :param content: Содержимое файла, представленное в виде строки.
    :param existing_ids: Множество существующих идентификаторов.
    """
    matches = EMPTY_EXTERNAL_ID_PATTERN.findall(content)
    for _ in matches:
        new_id = generate_unique_five_digit_id(existing_ids)
        existing_ids.add(new_id)
        content = EMPTY_EXTERNAL_ID_PATTERN.sub(
            f"@ExternalId={new_id}\n", content, count=1
        )
    return content


def process_file(file_path, existing_ids):
    """
    Обрабатывает файл: ищет и заменяет пустые @ExternalId на уникальные значения.
    :param file_path:Путь к фича файлу, который необходимо обработать.
    :param existing_ids: Множество существующих идентификаторов.
    """
    file = Path(file_path)
    content = file.read_text(encoding="utf-8")

    extract_existing_ids(content, existing_ids)

    new_content = replace_empty_external_ids(content, existing_ids)

    if new_content != content:
        file.write_text(new_content, encoding="utf-8")


def main(files):
    """
    Основной метод, который обрабатывает файлы и подставляет уникальные идентификаторы.
    :param files: Список строк, представляющих пути к фича файлам
    """
    existing_ids = set()
    for file in files:
        process_file(file, existing_ids)


if __name__ == "__main__":
    import sys

    files = sys.argv[1:]
    main(files)
