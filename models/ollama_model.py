"""Ollama model wrapper for local testing."""

from __future__ import annotations

import os

import ollama

MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.1")


def query_model(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]
