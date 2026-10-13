# grok-api-python

**Project URL:** https://roadmap.sh/projects/openai-api-python

A small Python app that sends prompts to the [Grok API](https://docs.x.ai/) (xAI) and prints the responses, plus a script for experimenting with system prompts, temperature, and token limits.

## Features

- `main.py` — send a single prompt, get a response, see token usage
- `experiments.py` — compare system prompts, temperature values, and max-token limits
- API key stored in `.env` (never committed)

## Setup

### 1. Create the project (already done in this repo)

```
grok-api-python/
├── .env.example     # template for your secrets
├── .gitignore
├── requirements.txt
├── main.py          # send prompt → receive response
└── experiments.py   # system prompts / temperature / tokens
```

### 2. Set up Python

```powershell
cd grok-api-python
py -m venv .venv
.\.venv\Scripts\Activate.ps1      # if activation is blocked: Set-ExecutionPolicy -Scope Process RemoteSigned
pip install -r requirements.txt
```

### 3. Configure the Grok API

1. Create an API key at <https://console.x.ai/>
2. Copy the template and paste your key:

```powershell
Copy-Item .env.example .env
notepad .env
```

```
GROK_API_KEY=xai-...
GROK_MODEL=grok-4
GROK_BASE_URL=https://api.x.ai/v1
```

`.env` is listed in `.gitignore`, so your key stays out of Git.

## Usage

```powershell
python main.py "Explain recursion with a short example"

# or be prompted for input
python main.py

# tweak the settings
python main.py "Write a haiku about the ocean" --system "You are a poet." --temperature 1.2 --max-tokens 200
```

Example output:

```
--- Response
...

--- Usage ---
model: grok-4 | prompt tokens: 31 | completion tokens: 187 | total: 218
```

## Experiments

```powershell
python experiments.py                    # run everything
python experiments.py system             # only system prompts
python experiments.py temperature        # only temperature sweep
python experiments.py tokens             # only token-limit sweep
```

| Experiment  | What it varies                          | What to look for                       |
| ----------- | --------------------------------------- | -------------------------------------- |
| `system`    | neutral / expert / child personas       | tone, vocabulary, detail level         |
| `temperature` | 0.0 / 0.7 / 1.5                        | determinism vs. creativity             |
| `tokens`    | 50 / 200 / 800                          | `finish_reason` and truncation         |

## Git

```powershell
git init
git add .
git commit -m "Initial commit: Grok API starter with experiments"
```

## Publish to GitHub

```powershell
gh repo create grok-api-python --public --source=. --push
```

Or create the repo on <https://github.com/new>, then:

```powershell
git remote add origin https://github.com/<your-username>/grok-api-python.git
git branch -M main
git push -u origin main
```

## Notes

- The Grok API is OpenAI-compatible: `POST {base_url}/chat/completions` with `Authorization: Bearer <key>`.
- Model names change over time — see <https://docs.x.ai/docs/models> for current IDs.
- Errors (bad key, rate limit, invalid model) are surfaced with the API's message.
