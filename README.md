# Локальный AI-агент проверки кода на соответствие требованиям

Этот проект помогает проверить, насколько локальный репозиторий с кодом соответствует требованиям аналитика.

## Что умеет MVP
- Читает требования из `.txt`, `.md`, `.docx`, `.pdf`.
- Делит требования на атомарные пункты.
- Сканирует репозиторий и исключает «мусорные» директории/бинарные файлы.
- Индексирует код в чанки с путём и диапазоном строк.
- Для каждого требования ищет релевантные фрагменты кода (keyword + fallback similarity).
- Выполняет проверку через OpenAI API (или локальный fallback при `--no-ai`).
- Генерирует отчёт в `md`, `html`, `json`.

## Установка
1. Установите Python 3.11+.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте `.env` на основе примера:
   ```bash
   cp .env.example .env
   ```

## Настройка `.env`
```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
LOG_LEVEL=INFO
```

## Как запустить
Пример команды:
```bash
python app/main.py --requirements ./spec.docx --repo ./repo --output ./output/report.md --output-format md
```

Дополнительные аргументы:
- `--max-files 500`
- `--max-chunks-per-requirement 8`
- `--verbose`
- `--no-ai`
- `--include-tests`

## Где искать отчёт
Отчёт будет в пути, который указан в `--output`, например `./output/report.md`.

## Типичные ошибки
- `Unsupported requirements format` — неподдерживаемое расширение файла требований.
- `OpenAI client is not configured` — не указан `OPENAI_API_KEY` и запуск без `--no-ai`.
- Пустой отчёт — возможно, требования не распарсились или репозиторий пуст.

## TODO для масштабирования
- Подключить реальные embeddings + vector DB (FAISS/Qdrant/pgvector).
- Добавить параллельную обработку требований.
- Улучшить атомарный split требований через LLM parser.
- Добавить экспорт в DOCX/PDF.
- Добавить web UI.
- Ввести baseline-правила качества кода (линтеры/архитектурные паттерны).
