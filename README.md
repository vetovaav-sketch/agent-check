# Локальный AI-агент проверки кода на соответствие требованиям

Этот проект проверяет, насколько локальный репозиторий с кодом соответствует требованиям аналитика.

## Что уже работает
- Поддержка требований: `.txt`, `.md`, `.docx`, `.pdf`.
- Нормализация и разбиение требований на атомарные пункты (`R1`, `R2`, ...).
- Сканирование репозитория с исключением мусорных директорий и бинарных файлов.
- Индексация кода в чанки с метаданными: `file_path`, `line_start`, `line_end`, `code_excerpt`.
- Поиск релевантных фрагментов: keyword search + vector-like поиск + similarity fallback.
- Проверка по каждому требованию:
  - через OpenAI API (если есть ключ),
  - или локальный безопасный fallback (`--no-ai`).
- Отчёт в 3 форматах: `md`, `html`, `json`.

## Ограничения первой версии
- Локальный fallback-режим (`--no-ai`) эвристический: он не заменяет полноценную LLM-проверку.
- Vector search — облегчённый in-memory вариант (TF/нормализованные токены), без внешней vector DB.
- Для `.docx` и `.pdf` нужны зависимости `python-docx` и `pypdf`.

## Установка
1. Python 3.11+ (в репозитории зафиксирована `3.11.14` через `.python-version`).
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте `.env`:
   ```bash
   cp .env.example .env
   ```

## Пример `.env`
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
LOG_LEVEL=INFO
```

Если вы хотите запуск без OpenAI, оставьте ключ пустым и используйте `--no-ai`.

## Быстрый локальный запуск (шаг за шагом)

### 1) Запуск на демо-примере
```bash
python app/main.py \
  --requirements ./examples/spec_example.txt \
  --repo ./examples/demo_repo \
  --output ./output/demo_report.md \
  --output-format md \
  --no-ai \
  --verbose
```

### 2) Проверка своего репозитория
```bash
python app/main.py \
  --requirements ./spec.docx \
  --repo ./repo \
  --output ./output/report.md \
  --output-format md
```

### 3) Форматы отчёта
- `--output-format md`
- `--output-format html`
- `--output-format json`

## Дополнительные CLI-аргументы
- `--max-files 500`
- `--max-chunks-per-requirement 8`
- `--verbose`
- `--no-ai`
- `--include-tests`

## Примеры входных/выходных данных
- Пример требований: `examples/spec_example.txt`
- Пример тестового репозитория: `examples/demo_repo/`
- Пример итогового отчёта: `output/examples/report_example.md`

## Тесты
```bash
pytest -q
```

## Типичные ошибки
- `Unsupported requirements format` — формат файла требований не поддерживается.
- `OpenAI client is not configured` — не указан `OPENAI_API_KEY` и не передан `--no-ai`.
- Пустой отчёт — требования не распарсились или по ним не найдено релевантных фрагментов.

## TODO (следующая итерация)
- Подключение реальных embeddings API + FAISS/Qdrant/pgvector.
- Более строгий schema validation structured-ответа модели.
- Batch-проверка требований для ускорения.
- Экспорт отчёта в PDF/DOCX.
