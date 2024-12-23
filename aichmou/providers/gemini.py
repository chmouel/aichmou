#!/usr/bin/env python
# Author: Chmouel Boudjnah <chmouel@chmouel.com>

import google.generativeai as genai

from aichmou.common import get_pass_key

from .abstract_ai import AbstractAI


class Gemini(AbstractAI):
    model = "gemini-1.5-flash"

    def complete(self, prompt: str, text: str) -> str:
        api_key = self.api_key
        if self.api_key.startswith("pass::"):
            api_key = get_pass_key(self.api_key.split("::")[1])
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt % text)
        return response.text