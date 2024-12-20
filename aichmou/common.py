import argparse
import os
import select
import shutil
import subprocess
import sys
import tempfile

promptfr = """
Vous êtes un modèle conçu pour corriger uniquement les fautes de français dans un
texte. Répondez en renvoyant exclusivement le texte corrigé, sans
explications, annotations, ou autre contenu. 

Si vous ne pouvez pas corriger le texte, renvoyez-le tel quel, inchangé. 
Si le texte est en Markdown, conservez la mise en forme à tout prix.
Si le texte est en anglais, renvoyez la réponse en anglais.

Voici le texte à corriger :

%s
"""

prompten = """
You are a model designed to correct grammar, spelling, and syntax errors in
English text. Respond by returning only the corrected text, with no
explanations, annotations, or additional content. 
If the text cannot be corrected, return it unchanged. 
If the text is in Markdown, keep the formatting. 
Here is the text to correct:

%s
"""

promptgitcommit = """
Write a commit message categorizing the change as one of the following: 
- Feature: For new functionality or enhancements. 
- Bugfix: For bug resolutions or fixes. 
- Chore: For non-functional updates like refactoring or dependency upgrades. 
- Tests: For additions or updates to test cases.

Ensure:
- The title has a maximum of 50 characters.
- The detailed message is wrapped at 72 characters.
- The title and message are separated by a blank line.

Here is the diff:

%s
"""


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument(
        "-e",
        "--english",
        action="store_true",
        help="Set English to True",
    )
    parser.add_argument(
        "--git-commit",
        action="store_true",
        help="Generate a Git commit message",
    )
    parser.add_argument(
        "-g",
        "--graphical-diff",
        action="store_true",
        default=False,
        help="Do graphical diff with kitty",
    )
    parser.add_argument(
        "-t",
        "--text-diff",
        action="store_true",
        default=False,
        help="Show diff with git diff",
    )
    parser.add_argument(
        "-n",
        "--no-diff",
        action="store_true",
        default=True,
        help="No diff output",
    )
    parser.add_argument(
        "-C",
        "--no-clipboard-copy",
        action="store_true",
        default=False,
        help="No clipboard copy",
    )
    parser.add_argument(
        "--mistral", action="store_true", default=False, help="Use mistral"
    )
    parser.add_argument("--azure", action="store_true", default=False, help="Use Azure")
    parser.add_argument(
        "--openai", action="store_true", default=False, help="Use OpenAI"
    )
    parser.add_argument("--groq", action="store_true", default=False, help="Use Groq")
    parser.add_argument(
        "--groq-api-pass-key", default="groq/api", help="Groq API Key in pass store"
    )

    parser.add_argument("--gemini", action="store_true", default=False, help="Use Groq")
    parser.add_argument(
        "--gemini-api-pass-key",
        default="google/gemini-api",
        help="Gemini API Key in pass store",
    )
    args = parser.parse_args()
    return args


def get_prompt(args: argparse.Namespace) -> str:
    if args.english:
        return prompten
    elif args.git_commit:
        return promptgitcommit
    return promptfr


def get_pass_key(pass_key: str) -> str:
    """Get token from pass."""
    output: str = subprocess.check_output(f"pass show {pass_key}", shell=True).decode(
        "utf-8"
    )
    if not output:
        raise Exception(f"pass {pass_key} is empty or not found.")
    return output.strip()


def get_clipboard_text() -> str:
    if sys.platform == "darwin":
        return subprocess.check_output("pbpaste", shell=True).decode("utf-8").strip()
    elif sys.platform.startswith("linux"):
        return subprocess.check_output("wl-paste", shell=True).decode("utf-8").strip()
    else:
        raise NotImplementedError("Unsupported platform")


def set_clipboard_text(content: str):
    if sys.platform == "darwin":
        subprocess.run("pbcopy", input=content, text=True)
    elif sys.platform.startswith("linux"):
        subprocess.run("wl-copy", input=content, text=True)
    else:
        raise NotImplementedError("Unsupported platform")


def get_text() -> str:
    if select.select([ sys.stdin, ], [], [], 0.0,)[0]:  # fmt: skip
        text = sys.stdin.read().strip()
    else:
        text = get_clipboard_text()
        if not text:
            try:
                text = input("Enter text to correct: ")
            except KeyboardInterrupt:
                print("No input exiting")
                sys.exit(1)
    return text


def show_response(args: argparse.Namespace, oldcontent, content: str):
    if content.startswith('"'):
        content = content[1:]

    if content.endswith('"'):
        content = content[:-1]

    if not content:
        return

    oldcontent = oldcontent.strip()
    content = content.strip()

    if oldcontent == content:
        return

    if not args.no_diff:
        diff = diff_content(args, oldcontent, content).strip()
        if diff:
            print(diff)

    if args.no_clipboard_copy:
        print(content)
    else:
        set_clipboard_text(content)


def diff_content(args: argparse.Namespace, content: str, new: str) -> str:
    # Create temporary files
    with (
        tempfile.NamedTemporaryFile(delete=False) as old_file,
        tempfile.NamedTemporaryFile(delete=False) as new_file,
    ):
        old_file_name = old_file.name
        new_file_name = new_file.name
        old_file.write(content.encode())
        new_file.write(new.encode())

    # Determine which diff tool to use
    diff_tool = "diff"
    diff_args = "-u"

    diff_tool = "git"
    diff_args = [
        "-c",
        "core.pager=cat",
        "diff",
        "--no-index",
        "--color=always",
        "--word-diff=color",
        "--word-diff-regex=.",
    ]

    if args.graphical_diff and shutil.which("kitten"):
        diff_tool = "kitten"
        diff_args = ["diff"]

    if args.text_diff:
        diff_tool = "diff"
        diff_args = ["-u"]

    # Perform the diff
    try:
        result = subprocess.run(
            [diff_tool] + diff_args + [old_file_name, new_file_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        diff_output = result.stdout
    except subprocess.CalledProcessError as e:
        diff_output = e.stdout + e.stderr

    # Clean up temporary files
    finally:
        try:
            os.remove(old_file_name)
            os.remove(new_file_name)
        except OSError:
            pass
    if diff_tool == "kitten":
        return ""

    diff = pipe_to_diff_tool(diff_output)
    if """\\ No newline at end of file""" in diff:
        diff = diff.replace("""\\ No newline at end of file""", "")
    return diff


def pipe_to_diff_tool(content):
    # Check if delta or diff-so-fancy is available
    diff_tool = "cat"
    diff_args = []
    if shutil.which("diff-so-fancy"):
        diff_tool = "diff-so-fancy"
    if shutil.which("delta"):
        diff_tool = "delta"
        diff_args = ["--file-style=omit", "--hunk-header-style=omit"]

    if diff_tool:
        # Pipe the content to the diff tool
        process = subprocess.Popen(
            [diff_tool] + diff_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(input=content.encode())
        if process.returncode == 0:
            return stdout.decode()
        else:
            raise RuntimeError(f"Error running {diff_tool}: {stderr.decode()}")
    else:
        raise RuntimeError("Neither 'delta' nor 'diff-so-fancy' is installed")
