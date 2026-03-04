"""OpenAI model wrapper."""

from __future__ import annotations

import os

from openai import OpenAI

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
_client = OpenAI()


def query_model(prompt: str) -> str:
    response = _client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content or ""
