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
Here is the result of running `git diff
--cached`. Based on this, suggest a **Conventional Commit message**. Ensure the
message includes both a clear title describing the change and make sure a body
explaining the change, do not invent anything new just try to comprehend the
diff and explain it.

Do not include any additional text outside the commit message.

# Conventional Commits 1.0.0

## Summary

Conventional Commits is a specification for commit messages that follows
these rules to ensure clarity and consistency:

### Format
<type>[optional scope]: <description>

[body]

### Types
1. **fix:** A bug fix correlating to a PATCH version.
2. **feat:** A new feature correlating to a MINOR version.

Other types include:  
- **build:** Changes to build systems or dependencies.  
- **chore:** Maintenance tasks (e.g., dependency updates).  
- **ci:** Changes to CI configuration.  
- **refactor:** Code changes not adding features or fixing bugs.  
- **test:** Changes to or addition of tests.  

Here is the result of `git diff --cached`:
%s
"""

DEFAULT = """You are a helpful assistant.
Here is my question I would like help with, be as succinct as possible:

###
%s
###
"""
