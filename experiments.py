"""Experiments: system prompts, temperature, and token limits.

Each experiment sends the same core prompt with varied settings so you can
compare the outputs side by side.

Usage:
    python experiments.py                 # run all experiments
    python experiments.py temperature      # run one group
    python experiments.py system temperature tokens
"""

import sys

from main import ask_grok, load_config

CORE_PROMPT = "Explain how HTTP cookies work in exactly two sentences."

SYSTEM_PROMPTS = {
    "neutral": "You are a helpful assistant.",
    "expert": (
        "You are a senior network engineer. Answer with precision and use "
        "correct technical terminology."
    ),
    "child": (
        "You are explaining to a 10-year-old. Use simple words and a friendly tone."
    ),
}

TEMPERATURES = [0.0, 0.7, 1.5]
MAX_TOKENS_LIST = [50, 200, 800]


def banner(title: str) -> None:
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def run_system_prompts(cfg: dict) -> None:
    for name, system in SYSTEM_PROMPTS.items():
        banner(f"System prompt: {name}")
        data = ask_grok(CORE_PROMPT, system_prompt=system, temperature=0.7, **cfg)
        print(data["choices"][0]["message"]["content"].strip())


def run_temperatures(cfg: dict) -> None:
    for temp in TEMPERATURES:
        banner(f"Temperature: {temp}")
        data = ask_grok(CORE_PROMPT, temperature=temp, **cfg)
        print(data["choices"][0]["message"]["content"].strip())


def run_token_limits(cfg: dict) -> None:
    for limit in MAX_TOKENS_LIST:
        banner(f"Max tokens: {limit}")
        try:
            data = ask_grok(CORE_PROMPT, temperature=0.7, max_tokens=limit, **cfg)
        except RuntimeError as exc:
            print(f"(stopped early) {exc}")
            continue
        choice = data["choices"][0]
        content = choice["message"]["content"].strip()
        finish = choice.get("finish_reason", "unknown")
        print(f"[finish_reason: {finish}]\n{content}")


EXPERIMENTS = {
    "system": run_system_prompts,
    "temperature": run_temperatures,
    "tokens": run_token_limits,
}


def main() -> None:
    api_key, model, base_url = load_config()
    cfg = {"api_key": api_key, "model": model, "base_url": base_url}

    names = [n.lower() for n in sys.argv[1:]] or list(EXPERIMENTS)
    unknown = [n for n in names if n not in EXPERIMENTS]
    if unknown:
        sys.exit(f"Unknown experiment(s): {', '.join(unknown)}\n"
                 f"Choose from: {', '.join(EXPERIMENTS)}")

    for name in names:
        EXPERIMENTS[name](cfg)


if __name__ == "__main__":
    main()
