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
You are an expert programmer, and you are trying to title a pull request.
You went over every file that was changed in it.
For some of these files changes were too big and were omitted in the files diff summary.
Please summarize the pull request into a single specific theme.
Write your response using the imperative tense following the kernel git commit style guide.
Write a high level title.
Do not repeat the commit summaries or the file summaries.
Do not list individual changes in the title.

EXAMPLE SUMMARY COMMENTS:
```
Raise the amount of returned recordings
Switch to internal API for completions
Lower numeric tolerance for test files
Schedule all GitHub actions on all OSs
```

THE FILE SUMMARIES:
###
%s
###

Remember to write only one line, no more than 50 characters.
"""

DEFAULT = """You are a helpful assistant.
Here is my question I would like help with, be as succinct as possible:

###
%s
###
"""
