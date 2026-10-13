"""grok-api-python - send a prompt to the Grok API and print the response."""

import argparse
import os
import sys

import requests
from dotenv import load_dotenv

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful assistant. Be concise and accurate."
)


def load_config() -> tuple[str, str, str]:
    """Load API key, model, and base URL from the environment / .env file."""
    load_dotenv()

    api_key = os.getenv("GROK_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here":
        sys.exit(
            "Error: GROK_API_KEY is not set.\n"
            "Copy .env.example to .env and add your key from https://console.x.ai/"
        )

    model = os.getenv("GROK_MODEL", "grok-4").strip()
    base_url = os.getenv("GROK_BASE_URL", "https://api.x.ai/v1").strip().rstrip("/")
    return api_key, model, base_url


def ask_grok(
    prompt: str,
    *,
    api_key: str,
    base_url: str,
    model: str,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> dict:
    """Send a single-turn chat completion request to the Grok API."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{base_url}/chat/completions",
        json=payload,
        headers=headers,
        timeout=60,
    )

    if response.status_code != 200:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"API error {response.status_code}: {detail}")

    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send a prompt to the Grok API and print the response."
    )
    parser.add_argument("prompt", nargs="?", help="The user prompt to send")
    parser.add_argument(
        "-s", "--system", default=DEFAULT_SYSTEM_PROMPT, help="System prompt"
    )
    parser.add_argument(
        "-t", "--temperature", type=float, default=0.7, help="Temperature (0-2)"
    )
    parser.add_argument(
        "-m", "--max-tokens", type=int, default=1024, help="Max tokens to generate"
    )
    parser.add_argument("--model", default=None, help="Override GROK_MODEL")
    args = parser.parse_args()

    prompt = args.prompt or input("Prompt: ").strip()
    if not prompt:
        sys.exit("No prompt given.")

    api_key, model, base_url = load_config()
    model = args.model or model

    try:
        data = ask_grok(
            prompt,
            api_key=api_key,
            base_url=base_url,
            model=model,
            system_prompt=args.system,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    except (RuntimeError, requests.RequestException) as exc:
        sys.exit(f"Request failed: {exc}")

    choice = data["choices"][0]
    print("\n--- Response ---")
    print(choice["message"]["content"].strip())

    usage = data.get("usage", {})
    if usage:
        print(
            "\n--- Usage ---\n"
            f"model: {model} | prompt tokens: {usage.get('prompt_tokens')} | "
            f"completion tokens: {usage.get('completion_tokens')} | "
            f"total: {usage.get('total_tokens')}"
        )


if __name__ == "__main__":
    main()
