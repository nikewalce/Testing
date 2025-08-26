from faker import Faker

fake = Faker("ru_RU")


def generate_text_by_size(size: str) -> str:
    """
    Генерирует текст в зависимости от указанного размера.
    :param size: Тип текста ("до 2 КБ" или "больше 2 КБ").
    :return: Сгенерированный текст.
    """
    text = ""
    if size == "до 2 КБ":
        target_size = 2048
    elif size == "больше 2 КБ":
        target_size = 3000
    else:
        raise ValueError(
            "Неверный параметр для размера текста. Используйте 'до 2 КБ' или 'больше 2 КБ'."
        )

    while len(text.encode("utf-8")) < target_size:
        text += fake.text(max_nb_chars=500)
    print(text)
    return text[:target_size]
