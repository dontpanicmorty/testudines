# Git safety rules for this repository

These rules are absolute and override any general assumption that finishing
a task includes committing/pushing it.

1. **Never stage, commit, or push any change on the `main` branch.** If work
   needs to happen, do it on a separate branch, or ask the developer how
   they want to branch it before touching git at all.
2. **Never stage, commit, or push any change without the developer's
   express, explicit confirmation for that specific action, given in that
   specific conversation.** A prior approval for one commit/push does not
   carry over to the next one — ask again every time. Completing the
   underlying file edits is not the same as being authorized to commit
   them; those are two separate steps requiring two separate green lights.

If in doubt, leave the changes staged/unstaged in the working tree and ask
before running `git commit` or `git push`.
