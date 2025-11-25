#!/usr/bin/env python3
"""
Health Check Script for Verridian Legal AI
==========================================

Verifies all system components are running correctly.

Usage:
    python scripts/health_check.py
"""

import os
import sys
import json
import requests
from pathlib import Path
from typing import Tuple, Optional
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def check_mark(passed: bool) -> str:
    """Return check or cross mark."""
    return "[PASS]" if passed else "[FAIL]"


def check_langfuse() -> Tuple[bool, str]:
    """Check if LangFuse server is running."""
    host = os.getenv("LANGFUSE_HOST", "http://localhost:3001")

    try:
        response = requests.get(f"{host}/api/public/health", timeout=5)
        if response.status_code == 200:
            return True, f"LangFuse server at {host}"
        return False, f"LangFuse returned status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, f"Cannot connect to LangFuse at {host}"
    except Exception as e:
        return False, f"LangFuse error: {str(e)}"


def check_langfuse_credentials() -> Tuple[bool, str]:
    """Check if LangFuse credentials are configured."""
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY", "")

    if public_key and secret_key:
        return True, f"Public key: {public_key[:12]}..."
    elif public_key:
        return False, "Secret key not set"
    elif secret_key:
        return False, "Public key not set"
    else:
        return False, "No LangFuse credentials found"


def check_database() -> Tuple[bool, str]:
    """Check if PostgreSQL database is accessible."""
    try:
        import psycopg2
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="langfuse",
            user="langfuse",
            password="langfuse_password",
            connect_timeout=5,
        )
        conn.close()
        return True, "PostgreSQL connected on port 5433"
    except ImportError:
        return None, "psycopg2 not installed (optional)"
    except Exception as e:
        return False, f"Database error: {str(e)}"


def check_gsw_workspace() -> Tuple[bool, str]:
    """Check if GSW workspace file exists and is valid."""
    data_dir = os.getenv("DATA_DIR", str(project_root / "data"))
    workspace_paths = [
        Path(data_dir) / "processed" / "gsw_workspace.json",
        Path(data_dir) / "processed" / "graph_snapshot.json",
        project_root / "data" / "processed" / "gsw_workspace.json",
    ]

    for path in workspace_paths:
        if path.exists():
            try:
                with open(path) as f:
                    data = json.load(f)

                actors = len(data.get("actors", {}))
                states = len(data.get("states", {}))
                questions = len(data.get("questions", {}))

                return True, f"Loaded: {actors} actors, {states} states, {questions} questions"
            except json.JSONDecodeError:
                return False, f"Invalid JSON in {path}"
            except Exception as e:
                return False, f"Error reading workspace: {str(e)}"

    return False, "No GSW workspace file found"


def check_embeddings_model() -> Tuple[bool, str]:
    """Check if embeddings model is available."""
    try:
        from sentence_transformers import SentenceTransformer

        model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

        # Check if model is cached
        from sentence_transformers.util import snapshot_download

        # Try loading the model
        start = time.time()
        model = SentenceTransformer(model_name)
        load_time = time.time() - start

        return True, f"{model_name} loaded in {load_time:.1f}s"
    except ImportError:
        return None, "sentence-transformers not installed"
    except Exception as e:
        return False, f"Embeddings error: {str(e)}"


def check_llm_connection() -> Tuple[bool, str]:
    """Check if LLM API is accessible."""
    api_key = os.getenv("OPENROUTER_API_KEY", "")

    if not api_key:
        return False, "OPENROUTER_API_KEY not set"

    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )

        if response.status_code == 200:
            return True, "OpenRouter API accessible"
        elif response.status_code == 401:
            return False, "Invalid API key"
        else:
            return False, f"API returned status {response.status_code}"
    except Exception as e:
        return False, f"LLM connection error: {str(e)}"


def check_ui_server() -> Tuple[bool, str]:
    """Check if UI development server is running."""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            return True, "UI server running on port 3000"
        return False, f"UI returned status {response.status_code}"
    except requests.exceptions.ConnectionError:
        return None, "UI server not running (optional)"
    except Exception as e:
        return False, f"UI error: {str(e)}"


def check_corpus_data() -> Tuple[bool, str]:
    """Check if corpus data exists."""
    data_dir = Path(os.getenv("DATA_DIR", str(project_root / "data")))
    processed_dir = data_dir / "processed"

    if not processed_dir.exists():
        return False, "data/processed directory not found"

    jsonl_files = list(processed_dir.glob("*.jsonl"))
    json_files = list(processed_dir.glob("*.json"))

    if jsonl_files or json_files:
        file_count = len(jsonl_files) + len(json_files)
        total_size = sum(f.stat().st_size for f in jsonl_files + json_files)
        size_mb = total_size / (1024 * 1024)
        return True, f"{file_count} files, {size_mb:.1f} MB total"

    return False, "No data files in processed directory"


def check_python_dependencies() -> Tuple[bool, str]:
    """Check critical Python dependencies."""
    required = [
        "pydantic",
        "torch",
        "requests",
        "asyncio",
    ]

    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        return False, f"Missing packages: {', '.join(missing)}"
    return True, f"All {len(required)} core packages installed"


def run_health_checks():
    """Run all health checks and display results."""
    print("\n" + "=" * 60)
    print("VERRIDIAN LEGAL AI - HEALTH CHECK")
    print("=" * 60 + "\n")

    checks = [
        ("Python Dependencies", check_python_dependencies),
        ("LangFuse Server", check_langfuse),
        ("LangFuse Credentials", check_langfuse_credentials),
        ("PostgreSQL Database", check_database),
        ("GSW Workspace", check_gsw_workspace),
        ("Corpus Data", check_corpus_data),
        ("Embeddings Model", check_embeddings_model),
        ("LLM Connection", check_llm_connection),
        ("UI Server", check_ui_server),
    ]

    results = []

    for name, check_fn in checks:
        try:
            passed, message = check_fn()

            if passed is None:
                status = "[SKIP]"
            elif passed:
                status = "[PASS]"
            else:
                status = "[FAIL]"

            results.append((name, passed, message))
            print(f"{status} {name}")
            print(f"       {message}\n")
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"[ERR]  {name}")
            print(f"       Error: {str(e)}\n")

    # Summary
    print("=" * 60)
    passed = sum(1 for _, p, _ in results if p is True)
    failed = sum(1 for _, p, _ in results if p is False)
    skipped = sum(1 for _, p, _ in results if p is None)

    print(f"SUMMARY: {passed} passed, {failed} failed, {skipped} skipped")

    if failed == 0:
        print("\nSystem is healthy and ready!")
        return 0
    else:
        print("\nSome checks failed. See above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(run_health_checks())
