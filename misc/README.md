## Misc

## Alfred Workflow

You can install the alfred workflow but you probably want to customize it to
launch where the virtual env is located, this is what i use for example (to be filled in the Run Script):

```bash
cat <<EOF|$HOME/go/src/gitlab.com/chmouel/aichmou/.venv/bin/python3 $HOME/go/src/gitlab.com/chmouel/aichmou/ai spell
{query}
EOF
```
