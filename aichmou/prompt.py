SPELL_FR = """
Vous êtes un modèle conçu pour corriger uniquement les fautes de français dans un
texte. Répondez en renvoyant exclusivement le texte corrigé, sans
explications, annotations, ou autre contenu. 

Si vous ne pouvez pas corriger le texte, renvoyez-le tel quel, inchangé. 
Si le texte est en Markdown, conservez la mise en forme à tout prix.
Si le texte est en anglais, renvoyez la réponse en anglais.

Voici le texte à corriger :

%s
"""

SPELL_EN = """
You are a model designed to correct grammar, spelling, and syntax errors in
English text. Respond by returning only the corrected text, with no
explanations, annotations, or additional content. 
If the text cannot be corrected, return it unchanged. 
If the text is in Markdown, keep the formatting. 
Here is the text to correct:

%s
"""

GIT_COMMIT = """
Write commit message for the change with commitizen convention. Make sure the
title has maximum 50 characters and message is wrapped at 72 characters. Be
brief and don't output anything else than the git commit message.

Here is the git commit diff output:

%s
"""
