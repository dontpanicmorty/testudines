# Known Gaps

Tracked list of things left unfinished or unverified in SQL Dojo. Update this file as items are closed.

## Integrity gaps

- [ ] **Import doesn't verify completion claims.** Export/Import (sidebar buttons) round-trip the current user's `progress` blob as plain JSON with no validation on the way back in — `Import` does `progress = JSON.parse(text); saveProgress();` and trusts it completely. Anyone can open an exported file, hand-edit every `completed` flag to `true`, and re-import it to show 100%/300 without having solved anything.

  Fundamental limitation to design against: `curriculum.js` (and thus every `solutionSql`) ships in cleartext inside the app bundle, and the in-app "Show solution" button reveals it too — so no purely client-side check can ever prove "solved without seeing the answer." Every option below has to be judged against that ceiling, not an impossible airtight one.

  Options considered:
  1. **Re-execute each imported module's saved `code` against its real `schemaSql`/`solutionSql` at import time** (the same check `handleCheck` already does live), and only keep `completed: true` if it actually verifies. Raises the bar from "flip one boolean" to "have a syntactically working query per module" — real friction, no new infrastructure — but doesn't stop someone who copy-pastes `solutionSql` straight out of `curriculum.js` for every module, since that trivially passes too.
  2. **Sign/hash the exported file** so hand-edited files are detectable. Sounds stronger but any secret used to compute the signature has to live in the client JS itself, readable by anyone who opens `index.html` — stops only the most casual tampering, not anyone who looks at the source. Weak.
  3. **Server-side verification** (grading and the completion ledger live off the user's machine, like LeetCode/HackerRank) — the only approach that's actually robust against a determined local attacker. Requires giving this app a backend, accounts, and a network dependency, directly contradicting its "zero runtime network dependency, fully offline" design. Disproportionate for a personal practice tool.
  4. **Behavioral heuristics** (flag imports claiming completion with implausibly little elapsed time or Run-attempt count, using data the app already tracks). Soft signal, trivially gamed by padding the fake data further — reasonable as an *additional* red flag layered on top of another option, not standalone.
  5. **Never trust `completed: true` from an imported file at all** — only restore `code`/`failCount`, force a live re-Check for credit. Strictly more user friction than option 1 for the identical guarantee (if the code is genuinely correct, auto-verifying it vs. making the user click Check again proves the same thing), so dominated by option 1.
  6. **Track whether "Show solution" was ever revealed for a module**, as a transparency signal rather than a security boundary. Doesn't defend against tampering, but gives anyone reviewing someone else's progress real signal ("completed, but only after seeing the answer" vs. clean) that no verification check can provide.

  **Recommendation**: combine 1 + 6. Re-executing code at import closes the realistic threat (casual tampering, not a determined adversary willing to read source), and solution-reveal tracking adds honest signal beyond what any check can enforce. Not yet implemented.
