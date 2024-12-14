import argparse
import os
import shutil
import subprocess
import sys
import tempfile

promptfr = """
Tu es un modèle conçu pour corriger uniquement les fautes de français dans un
texte. Réponds en renvoyant exclusivement le texte corrigé, sans
explications, annotations, ou autre contenu. 

Si tu ne peux pas corriger le texte, renvoie-le tel quel, inchangé. 
Si le texte est en Markdown, conserve la mise en forme à tout prix.

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


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument(
        "-e",
        "--english",
        action="store_true",
        help="Set English to True",
    )
    parser.add_argument(
        "-g", "--graphical-diff", action="store_true", help="graphical-diff"
    )
    args = parser.parse_args()
    return args


def get_prompt(args: argparse.Namespace) -> str:
    if args.english:
        return prompten
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
    diff = diff_content(args, oldcontent.strip(), content).strip()
    if diff:
        print(diff)
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
