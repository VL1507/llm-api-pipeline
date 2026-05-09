import csv
import json
import logging
from pathlib import Path
from typing import Any, cast

from openai import OpenAI

from config import LLM_MODEL, ZVENOAI_API_KEY
from utils import get_custom_logger

logger = get_custom_logger(__name__)


client = OpenAI(
    base_url="https://api.zveno.ai/v1",
    api_key=ZVENOAI_API_KEY,
)

SYSTEM_PROMPT = """Ты профессиональный классификатор отзывов.
На вход получаешь текстовый отзыв, возвращаешь ТОЛЬКО json.
Формат json:
{
    "tonality": <positive/negative/neutral>,
    "topic": <Тема отзыва, 1-5 слов>,
    "factor": ["factor1", "factor2", ...],
    "confidence": <число от 0.0 до 1.0, уверенность в правильности классификации>
}

factor - то что оценил пользователь, 1-2 слова на один фактор, может быть пустым.
"""  # noqa: RUF001


def review_classification(review: str) -> dict[str, Any]:
    """
    Классификация отзывов.

    Returns:
        dict[str, Any]

    """
    completion = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": review},
        ],
    )
    answer_txt = completion.choices[0].message.content

    if answer_txt is None:
        logger.error("Не пришел ответ от llm")  # noqa: RUF001
        return {"error": "Не пришел ответ от llm"}  # noqa: RUF001

    try:
        return cast("dict[str, Any]", json.loads(answer_txt))
    except json.decoder.JSONDecodeError:
        logger.exception("Ошибка декодирования. Текст: %s", review)
        return {"error": "Ошибка декодирования"}


def read_csv(path: str | Path) -> list[tuple[str, str]]:
    """
    Читает csv с отзывами.

    Returns:
        list[tuple[str, str]]

    """  # noqa: RUF002
    with Path(path).open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        return [(row["id"], row["review"]) for row in reader]


def write_json(path: str | Path, data: list[dict[str, Any]]) -> None:
    """Записывает результат в json."""
    Path(path).write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def main() -> None:
    """Запускает анализ отзывов."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    input_data = read_csv("review.csv")

    output_data: list[dict[str, Any]] = []

    for id_, review in input_data:
        res = review_classification(review)
        logger.info("Отзыв id=%s проанализирован", id_)
        output_data.append({"id": id_, **res})

    write_json("result.json", output_data)


if __name__ == "__main__":
    main()
