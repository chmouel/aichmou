#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>
import shutil
import subprocess


from .abstract_ai import AbstractAI


class ChatGPT(AbstractAI):
    command = "gh-gpt"

    def complete(self, prompt: str, text: str) -> str:
        if shutil.which(self.command) is None:
            raise Exception("gh-gpt not found, please install it")

        process = subprocess.Popen(
            [self.command],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        input_data = f"{prompt} {text}".encode("utf-8")
        output, error = process.communicate(input=input_data)

        if process.returncode != 0:
            raise Exception(f"Error running gh-gpt: {error.decode('utf-8')}")

        return output.decode("utf-8")
