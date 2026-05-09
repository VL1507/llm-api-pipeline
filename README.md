# Лабораторная работа: API-пайплайн: данные → LLM → результат

[Задание](./docs/task.md)

## Возможности

Принимает `csv` файл формата `id;review`. Возвращает `json` файл содержащий список элементов одного из трех видов:

1. Валидный ответ

```json
{
    "tonality": <positive/negative/neutral>,
    "topic": <Тема отзыва, 1-5 слов>,
    "factor": ["factor1", "factor2", ...],
    "confidence": <число от 0.0 до 1.0, уверенность в правильности классификации>
}
```

factor - то что оценил пользователь, 1-2 слова на один фактор, может быть пустым.

2. LLM не ответил

```json
{"error": "Не пришел ответ от llm"}
```

3. LLM ответил не в формате json

```json
{"error": "Ошибка декодирования"}
```

## Установка, настройка и запуск

### Установка

```bash
git clone https://github.com/VL1507/llm-api-pipeline.git

cd llm-api-pipeline
```

### Настройка

```bash
cp .env.example .env
```

- `ZVENOAI_API_KEY` можно создать по ссылке [ZvenoAI](https://zveno.ai/api-keys)
- `LLM_MODEL` можно выбрать модель из [списка](https://zveno.ai/models)

### Запуск

```bash
# Установка uv
pip install uv

# Установка библиотек
uv sync

# Запуск анализатора отзывов
uv run .\src\main.py
```
