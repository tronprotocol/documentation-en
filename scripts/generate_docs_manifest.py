#!/usr/bin/env python3
"""Generate the machine-readable documentation manifest published by MkDocs."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

import yaml


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = REPOSITORY_ROOT / "docs"
MKDOCS_CONFIG = REPOSITORY_ROOT / "mkdocs.yml"
DEFAULT_OUTPUT_PATH = REPOSITORY_ROOT / "site" / "docs-manifest.json"
SITE_URL = "https://tronprotocol.github.io/documentation-en/"
SOURCE_ROOT = "https://raw.githubusercontent.com/tronprotocol/documentation-en/master/docs/"


def document_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if match:
        return re.sub(r"\s+#+$", "", match.group(1)).strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def nav_documents(items: list[object], top_section: str | None = None):
    """Yield Markdown paths and their top-level nav section in nav order."""
    for item in items:
        if isinstance(item, str):
            if item.endswith(".md"):
                yield Path(item), top_section or "Other"
            continue
        if not isinstance(item, dict):
            continue
        for label, value in item.items():
            section = top_section or str(label)
            if isinstance(value, str):
                if value.endswith(".md"):
                    yield Path(value), section
            elif isinstance(value, list):
                yield from nav_documents(value, section)


def configured_documents() -> list[tuple[Path, str]]:
    config = yaml.safe_load(MKDOCS_CONFIG.read_text(encoding="utf-8"))
    nav = config.get("nav")
    if not isinstance(nav, list):
        raise ValueError("mkdocs.yml must contain a list-valued nav section")

    documents = []
    seen = set()
    for relative_path, section in nav_documents(nav):
        if relative_path in seen:
            continue
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"Navigation page must stay inside docs/: {relative_path}")
        source_path = DOCS_ROOT / relative_path
        if not source_path.is_file():
            raise FileNotFoundError(f"Navigation page does not exist: {relative_path}")
        seen.add(relative_path)
        documents.append((relative_path, section))
    return documents


def html_url(relative_path: Path) -> str:
    if relative_path == Path("index.md"):
        suffix = ""
    elif relative_path.name == "index.md":
        suffix = relative_path.parent.as_posix().rstrip("/") + "/"
    else:
        suffix = relative_path.with_suffix("").as_posix().rstrip("/") + "/"
    return SITE_URL + quote(suffix, safe="/")


def markdown_url(relative_path: Path) -> str:
    return SOURCE_ROOT + quote(relative_path.as_posix(), safe="/")


def last_modified(source_path: str) -> str | None:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", source_path],
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    value = result.stdout.strip()
    return value or None


def build_manifest() -> dict[str, object]:
    documents = []
    for relative_path, section in configured_documents():
        path = DOCS_ROOT / relative_path
        source_path = (Path("docs") / relative_path).as_posix()
        documents.append(
            {
                "title": document_title(path),
                "section": section,
                "html_url": html_url(relative_path),
                "markdown_url": markdown_url(relative_path),
                "source_path": source_path,
                "last_modified": last_modified(source_path),
            }
        )

    return {
        "schema_version": 1,
        "project": "java-tron documentation",
        "language": "en",
        "site_url": SITE_URL,
        "source_repository": "https://github.com/tronprotocol/documentation-en",
        "source_branch": "master",
        "documents": documents,
        "machine_readable_assets": [
            {
                "name": "LLM entry index",
                "url": SITE_URL + "llms.txt",
                "source_path": "docs/llms.txt",
            },
            {
                "name": "HTTP OpenAPI specification",
                "url": SITE_URL + "api/openapi.yaml",
                "source_path": "docs/api/openapi.yaml",
            },
            {
                "name": "JSON-RPC OpenRPC specification",
                "url": SITE_URL + "api/openrpc.json",
                "source_path": "docs/api/openrpc.json",
            },
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="output path (default: site/docs-manifest.json)",
    )
    args = parser.parse_args()
    output_path = args.output if args.output.is_absolute() else REPOSITORY_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(build_manifest(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
