# Aichmou

Aichmou is a tool designed to correct text and generate git commit messages using various AI models.

## Installation

To install the dependencies, install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run:

```bash
uv sync
```

source the virtual

```bash
source .venv/bin/activate
```

## Usage

Aichmou provides two main subcommands: `spell` and `gitcommit`. Both subcommands share common options.

### Common Options

- `--no-diff`: Do not show diff.
- `--no-clipboard-copy`: Do not copy result to clipboard.
- `--graphical-diff`: Use graphical diff tool if available.
- `--text-diff`: Use text diff tool.

### Spell Subcommand

The `spell` subcommand is used to correct spelling and grammar in the provided text.

```bash
python -m aichmou.common spell [options]
```

### Gitcommit Subcommand

The `gitcommit` subcommand is used to generate a git commit message based on the provided diff.

```bash
python -m aichmou.common gitcommit [options]
```

### Example

To correct spelling and grammar:

```bash
echo "Ths is a smple txt." | aichmou spell
```

To generate a git commit message:

```bash
git diff | aichmou gitcommit
```

you can directly commit the currently staged and unstaged changes with the -c option:

```bash
aichmou gitcommit -c
```

it will let you edit the commit message in your editor afterward.

To just have a conversation with an answer

```bash
aichmou prompt
```

it will by default open your $EDITOR unless you pass some text to its standard input.

```bash

## Configuration

Aichmou can be configured to use different AI models by setting the appropriate flags:

- `--mistral`: Use Mistral
- `--azure`: Use Azure
- `--openai`: Use OpenAI
- `--chatgpt`: Use ChatGPT (requires `gh-gpt` command installed and configured)
- `--groq`: Use Groq
- `--gemini`: Use Gemini

If you want to use another OpenAI endpoint like for example using it with a local
ollama/lm-studio you can use the flag:

`--openai-api-url`

For example:

```bash
ai --openai-api-url http://localhost:1234/v1
```

Furthermore you can pass your own model with the flag `--model`

### API Keys

API keys can be stored in a password manager and retrieved using the `pass` command. For example:

```bash
pass insert github/chmouel-token
pass insert groq/api
pass insert google/gemini-api
```

The keys can then be referenced in the command options:

```bash
python -m aichmou.common spell --groq --groq-api-pass-key groq/api
```
