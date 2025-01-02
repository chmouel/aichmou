import argparse
import os
import select
import shutil
import subprocess
import sys
import tempfile

SERVER_URL = "https://models.inference.ai.azure.com"
DEFAULT_ORDERS = ["gemini", "azureai", "openai", "mistralai", "groq", "chatgpt"]
OPENAI_DEFAULT_MODEL = "gpt-4o-mini"


class PassKeyError(Exception):
    """Exception raised for errors in retrieving the pass key."""

    pass


class ClipboardError(Exception):
    """Exception raised for errors in clipboard operations."""

    pass


class DiffToolError(Exception):
    """Exception raised for errors in diff tool operations."""

    pass


def get_pass_key(pass_key: str) -> str:
    """Get token from pass."""
    try:
        output: str = subprocess.check_output(
            f"pass show {pass_key}", shell=True
        ).decode("utf-8")
    except subprocess.CalledProcessError as e:
        raise PassKeyError(f"Error retrieving pass key {pass_key}: {e}")

    if not output:
        raise PassKeyError(f"pass {pass_key} is empty or not found.")
    return output.strip()


def get_clipboard_text() -> str:
    try:
        if sys.platform == "darwin":
            return (
                subprocess.check_output("pbpaste", shell=True).decode("utf-8").strip()
            )
        elif sys.platform.startswith("linux"):
            if shutil.which("copyq"):
                try:
                    selection = (
                        subprocess.check_output("copyq selection", shell=True)
                        .decode("utf-8")
                        .strip()
                    )
                    if selection:
                        return selection
                except subprocess.CalledProcessError:
                    pass
            if shutil.which("wl-paste"):
                return (
                    subprocess.check_output("wl-paste", shell=True)
                    .decode("utf-8")
                    .strip()
                )
            raise ClipboardError("No clipboard tool found")
        else:
            raise ClipboardError("Unsupported platform")
    except subprocess.CalledProcessError as e:
        raise ClipboardError(f"Error getting clipboard text: {e}")


def set_clipboard_text(content: str):
    try:
        if sys.platform == "darwin":
            subprocess.run("pbcopy", input=content, text=True)
        elif sys.platform.startswith("linux"):
            subprocess.run("wl-copy", input=content, text=True)
        else:
            raise ClipboardError("Unsupported platform")
    except subprocess.CalledProcessError as e:
        raise ClipboardError(f"Error setting clipboard text: {e}")


def get_text() -> str:
    if select.select([ sys.stdin, ], [], [], 0.0,)[0]:  # fmt: skip
        text = sys.stdin.read().strip()
    else:
        text = get_clipboard_text()
        if not text:
            try:
                text = input("Enter text to correct: ")
            except KeyboardInterrupt:
                sys.stderr.write("No input exiting")
                sys.exit(1)
    return text


def show_response(args: argparse.Namespace, oldcontent, content: str) -> str:
    output = ""
    if content.startswith('"'):
        content = content[1:]

    if content.endswith('"'):
        content = content[:-1]

    if not content:
        return ""

    oldcontent = oldcontent.strip()
    content = content.strip()

    if oldcontent == content:
        return ""

    if not args.no_diff:
        diff = diff_content(args, oldcontent, content).strip()
        if diff:
            output += diff

    if not args.no_clipboard_copy:
        set_clipboard_text(content)

    if not args.no_output:
        output += content

    return output


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
    except Exception as e:
        raise DiffToolError(f"Error running diff tool: {e}")
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
