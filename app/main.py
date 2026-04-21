from __future__ import annotations

import argparse
import logging
from pathlib import Path

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
from app.retrieval.vector_store import InMemoryVectorStore
from app.utils.file_utils import ensure_parent_dir
from app.utils.logging_utils import setup_logging

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="AI-агент проверки соответствия кода требованиям")
    p.add_argument("--requirements", required=True, help="Путь к файлу требований (.txt/.md/.docx/.pdf)")
    p.add_argument("--repo", required=True, help="Путь к локальному репозиторию")
    p.add_argument("--output", required=True, help="Путь к отчету")
    p.add_argument("--output-format", choices=["md", "html", "json"], default="md")
    p.add_argument("--max-files", type=int, default=None)
    p.add_argument("--max-chunks-per-requirement", type=int, default=8)
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--no-ai", action="store_true")
    p.add_argument("--include-tests", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    cfg = load_config()
    setup_logging(cfg.log_level, args.verbose)

    logger.info("Чтение требований: %s", args.requirements)
    req_text = normalize_text(extract_text(args.requirements))
    requirements = split_into_requirements(req_text)
    logger.info("Найдено требований: %d", len(requirements))

    logger.info("Сканирование репозитория: %s", args.repo)
    files = scan_repository(args.repo, max_files=args.max_files, include_tests=args.include_tests)
    chunks = chunk_repository(files, args.repo)
    logger.info("Проиндексировано файлов=%d, чанков=%d", len(files), len(chunks))

    store = InMemoryVectorStore()
    store.add_chunks(chunks)
    client = OpenAIClient(cfg)

    results = []
    for req in requirements:
        relevant = find_relevant_chunks(req, chunks, store, args.max_chunks_per_requirement)
        result = check_requirement(req, relevant, client, use_ai=not args.no_ai)
        results.append(result)

    output = Path(args.output)
    ensure_parent_dir(output)

    if args.output_format == "md":
        render_markdown_report(results, str(output))
    elif args.output_format == "html":
        render_html_report(results, str(output))
    else:
        render_json_report(results, str(output))

    logger.info("Отчет готов: %s", output)


if __name__ == "__main__":
    main()
