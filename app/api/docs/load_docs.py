from pathlib import Path
from typing import Dict, Any

import yaml


def load_yaml_docs(file_path: str) -> Dict[str, Any]:
    """Загрузка документации из YAML файла"""
    docs_path = Path(__file__).parent / file_path
    with open(docs_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)


BOOKS_DOCS = load_yaml_docs('books_docs.yaml')
