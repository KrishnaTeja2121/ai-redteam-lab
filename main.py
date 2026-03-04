"""Run red-team attack prompts against a target model and score responses."""

from __future__ import annotations

import argparse
from statistics import mean
from typing import Callable, Dict, List

from attacks.prompt_injection import load_attacks
from evaluation.safety_score import SafetyResult, score_response

ModelQueryFn = Callable[[str], str]


def resolve_model(provider: str) -> ModelQueryFn:
    if provider == "openai":
        from models.openai_model import query_model as query_openai

        return query_openai
    if provider == "ollama":
        from models.ollama_model import query_model as query_ollama

        return query_ollama

    providers = ["openai", "ollama"]
    raise ValueError(f"Unsupported provider '{provider}'. Use one of: {', '.join(providers)}")


def run(provider: str) -> None:
    query = resolve_model(provider)
    attacks = load_attacks()

    results: List[SafetyResult] = []

    for prompt in attacks:
        response = query(prompt)
        safety = score_response(response)
        results.append(safety)

        print(f"ATTACK: {prompt}")
        print(f"VERDICT: {safety.verdict} | SCORE: {safety.score} | REASON: {safety.reason}")
        print(f"MODEL: {response}")
        print("-" * 80)

    pass_count = sum(1 for item in results if item.verdict == "PASS")
    fail_count = sum(1 for item in results if item.verdict == "FAIL")
    review_count = sum(1 for item in results if item.verdict == "REVIEW")
    avg_score = mean(item.score for item in results) if results else 0

    print("SUMMARY")
    print(f"Provider: {provider}")
    print(f"Total: {len(results)} | PASS: {pass_count} | FAIL: {fail_count} | REVIEW: {review_count}")
    print(f"Average Safety Score: {avg_score:.1f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Red Team Lab")
    parser.add_argument(
        "--provider",
        default="openai",
        choices=["openai", "ollama"],
        help="Model provider to evaluate.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.provider)
