# Aichmou

Aichmou is a tool designed to correct text and generate git commit messages
using various AI models.

## Installation

To install the dependencies, first install
[uv](https://docs.astral.sh/uv/getting-started/installation/) and then run:

```bash
uv sync
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

The `aichmou` command will be available within the virtual environment.

## Usage

Aichmou provides two main subcommands: `spell` and `gitcommit`. Both
subcommands share common options.

### Common Options

- `--no-diff`: Do not show diff.
- `--no-clipboard-copy`: Do not copy result to clipboard.
- `--graphical-diff`: Use graphical diff tool if available.
- `--text-diff`: Use text diff tool.

### Spell Subcommand

The `spell` subcommand is used to correct spelling and grammar in the provided text.

```bash
aichmou spell [options]
```

By default, it will use your clipboard content for spelling correction, or you can pass text to it:

```bash
echo "Ths is a smple txt." | aichmou spell
```

### Gitcommit Subcommand

The `gitcommit` subcommand is used to generate a git commit message based on the provided diff.

```bash
aichmou gitcommit [options]
```

You can commit the currently staged and unstaged changes directly with the `-c` option:

```bash
aichmou gitcommit -c
```

It will allow you to edit the commit message in your editor afterward.

### Prompt Subcommand

To have a conversation with an AI model:

```bash
aichmou prompt
```

If you don't pass any text, it will use your `$EDITOR`.

## Configuration

Aichmou can be configured to use different AI models by setting the appropriate flags:

- `--mistral`: Use Mistral
- `--azure`: Use Azure
- `--openai`: Use OpenAI
- `--chatgpt`: Use ChatGPT (requires `gh-gpt` command installed and configured)
- `--groq`: Use Groq
- `--gemini`: Use Gemini

If you want to use another OpenAI endpoint, for example, a local ollama/lm-studio, you can use the flag:

`--openai-api-url`

For example:

```bash
aichmou --openai-api-url http://localhost:1234/v1
```

Additionally, you can specify your own model with the `--model` flag.

### API Keys

API keys can be stored in a password manager and retrieved using the `pass` command. For example:

```bash
pass insert github/chmouel-token
pass insert groq/api
pass insert google/gemini-api
```

The keys can then be referenced in the command options:

```bash
aichmou spell --groq --groq-api-pass-key groq/api
```
