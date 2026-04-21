# Простой локальный агент проверки кода по требованиям

Это **локальный Python CLI**.

Без Docker. Без веб-интерфейса. Без БД. Только запуск из терминала.

---

## Что делает агент

1. Читает файл требований (`.txt`, `.md`, `.docx`, `.pdf`)
2. Делит требования на пункты (`R1`, `R2`, ...)
3. Сканирует репозиторий с кодом
4. Находит похожие куски кода
5. Строит отчет:
   - `Реализовано неправильно`
   - `Отсутствует или не найдено в коде`

---

## Что нужно установить

1. Python 3.11+
2. Зависимости:

```bash
pip install -r requirements.txt
```

---

## Настройка `.env`

Скопируйте пример:

```bash
cp .env.example .env
```

Если хотите проверку через OpenAI API, заполните `OPENAI_API_KEY`.
Если хотите запуск без OpenAI, используйте флаг `--no-ai`.

---

## Самый простой запуск (демо)

```bash
python app/main.py \
  --requirements ./examples/spec_example.txt \
  --repo ./examples/demo_repo \
  --output ./output/demo_report.md \
  --output-format md \
  --no-ai
```

После запуска отчет будет в файле `output/demo_report.md`.

---

## Запуск на вашем проекте

```bash
python app/main.py \
  --requirements ./spec.docx \
  --repo ./repo \
  --output ./output/report.md \
  --output-format md
```

Дополнительно:
- `--output-format md|html|json`
- `--max-files 500`
- `--max-chunks-per-requirement 8`
- `--include-tests`
- `--verbose`
- `--no-ai`

---

## Примеры файлов

- Пример требований: `examples/spec_example.txt`
- Пример маленького репозитория: `examples/demo_repo/`
- Пример отчета: `output/examples/report_example.md`

---

## Ограничения MVP

- В режиме `--no-ai` проверка упрощенная (эвристики), а не «умный аудит».
- Поиск кода простой: ключевые слова + похожесть текста.
- Это первая рабочая версия, сделанная для простого локального запуска.

---

## Проверка тестов

```bash
pytest -q
```

Если тесты не запускаются, проверьте, что зависимости установлены.
