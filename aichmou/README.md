
# Aichmou

Aichmou is a tool designed to correct text and generate git commit messages using various AI models.

## Installation

To install the dependencies, first install [uv](https://docs.astral.sh/uv/getting-started/installation/) and then run:

```bash
uv sync
```

Activate the virtual environment:

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

### Examples

To correct spelling and grammar:

```bash
echo "Ths is a smple txt." | aichmou spell
```

To generate a git commit message:

```bash
git diff | aichmou gitcommit
```

To directly commit the currently staged and unstaged changes with the `-c` option:

```bash
aichmou gitcommit -c
```

This will let you edit the commit message in your editor afterward.

## Configuration

Aichmou can be configured to use different AI models by setting the appropriate flags:

- `--mistral`: Use Mistral
- `--azure`: Use Azure
- `--openai`: Use OpenAI
- `--chatgpt`: Use ChatGPT (requires `gh-gpt` command installed and configured)
- `--groq`: Use Groq
- `--gemini`: Use Gemini

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

## License

[Apache-2.0](./LICENSE)

## Authors

### Chmouel Boudjnah

- Fediverse - <[@chmouel@chmouel.com](https://fosstodon.org/@chmouel)>
- Twitter - <[@chmouel](https://twitter.com/chmouel)>
- Blog  - <[https://blog.chmouel.com](https://blog.chmouel.com)>
