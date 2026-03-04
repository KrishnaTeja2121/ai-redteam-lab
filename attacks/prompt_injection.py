"""Load red-team attack prompts from dataset."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

DATASET_PATH = Path(__file__).resolve().parents[1] / "dataset" / "attack_prompts.json"


def load_attacks() -> List[str]:
    """Return the list of attack prompts."""
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        prompts = json.load(file)

    if not isinstance(prompts, list):
        raise ValueError("attack_prompts.json must contain a JSON array of strings.")

    return [str(prompt) for prompt in prompts]
