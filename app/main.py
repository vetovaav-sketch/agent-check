from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Позволяет запускать команду вида `python app/main.py ...` из корня проекта.
if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.analysis.requirement_checker import check_requirement
from app.config import load_config
from app.openai_client import OpenAIClient
from app.repo_reader.chunker import chunk_repository
from app.repo_reader.scanner import scan_repository
from app.reporting.html_report import render_html_report
from app.reporting.json_report import render_json_report
from app.reporting.markdown_report import render_markdown_report
from app.requirements_parser.extractor import extract_text
from app.requirements_parser.normalizer import normalize_text
from app.requirements_parser.splitter import split_into_requirements
from app.retrieval.search import find_relevant_chunks
from app.utils.file_utils import ensure_parent_dir
from app.utils.logging_utils import setup_logging

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    # Простой CLI без дополнительных сервисов.
    parser = argparse.ArgumentParser(description="Локальный агент проверки кода по требованиям")
    parser.add_argument("--requirements", required=True, help="Файл требований (.txt/.md/.docx/.pdf)")
    parser.add_argument("--repo", required=True, help="Путь к репозиторию с кодом")
    parser.add_argument("--output", required=True, help="Куда сохранить отчет")
    parser.add_argument("--output-format", choices=["md", "html", "json"], default="md")
    parser.add_argument("--max-files", type=int, default=None)
    parser.add_argument("--max-chunks-per-requirement", type=int, default=8)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--no-ai", action="store_true")
    parser.add_argument("--include-tests", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config()
    setup_logging(cfg.log_level, args.verbose)

    logger.info("1/5 Читаю требования: %s", args.requirements)
    req_text = normalize_text(extract_text(args.requirements))
    requirements = split_into_requirements(req_text)

    logger.info("2/5 Сканирую репозиторий: %s", args.repo)
    files = scan_repository(args.repo, max_files=args.max_files, include_tests=args.include_tests)

    logger.info("3/5 Разбиваю код на чанки")
    chunks = chunk_repository(files, args.repo)

    logger.info("4/5 Проверяю каждое требование")
    client = OpenAIClient(cfg)
    results = []
    for req in requirements:
        relevant = find_relevant_chunks(req, chunks, args.max_chunks_per_requirement)
        result = check_requirement(req, relevant, client, use_ai=not args.no_ai)
        results.append(result)

    logger.info("5/5 Формирую отчет")
    output = Path(args.output)
    ensure_parent_dir(output)

    if args.output_format == "md":
        render_markdown_report(results, str(output))
    elif args.output_format == "html":
        render_html_report(results, str(output))
    else:
        render_json_report(results, str(output))

    logger.info("Готово: %s", output)


if __name__ == "__main__":
    main()
