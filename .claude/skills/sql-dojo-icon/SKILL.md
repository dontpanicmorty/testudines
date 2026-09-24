---
name: sql-dojo-icon
description: Mandatory workflow for any change to the SQL Dojo application icon/artwork. Use this whenever generating, previewing, or editing the icon image (mountains, moon, sky, pagoda, text, etc.) under tauri/src-tauri/icons/ or any script that produces the source artwork for it.
---

# SQL Dojo icon: mandatory apply-and-verify workflow

## The mistake this skill exists to prevent

A real incident: several rounds of icon tweaks (moon size/position) were done
by generating a PNG into a scratch directory and showing the developer a
preview image, then waiting for confirmation before touching the real icon
set. Multiple rounds of "does this look right?" passed with no objection
recorded either way, and the actual app icon was never regenerated or
rebuilt. The developer had no way to tell from the running app or from the
committed icon files that anything had changed, because nothing had. Time
was wasted and trust was damaged — the developer accurately called this out
as a fundamental process failure, not a rendering-detail bug.

**The core error: treating "show a preview and ask if it looks right" as a
valid stopping point for icon work.** It is not. A preview render is a
mid-task checkpoint, never the deliverable.

## The rule

**Every icon change must reach the actual running application in the same
turn it is made — no exceptions, no "let me know if this looks right first"
pause.** Concretely, every icon edit does all of these steps, every time,
without waiting for separate developer confirmation in between:

1. Regenerate the source artwork (the full-size PNG).
2. Run `cargo tauri icon <path-to-png>` from
   `tauri/src-tauri/` to regenerate the real icon
   set in `src-tauri/icons/`.
3. Delete the unneeded generated variants (`ios/`, `android/`,
   `Square*.png`, `StoreLogo.png`) — same as every prior icon round in this
   project.
4. Rebuild via `tauri/build.sh`.
5. Clear the old log, launch the built `.app`, and confirm a clean
   diagnostic log (macOS: `~/Library/Logs/com.mauriceallen.sqldojo/sqldojo.log`
   showing the usual `initDuckDB: ... -> instantiate complete` sequence with
   no errors).
6. Only then report the change as done — and report it as something that
   already happened ("rebuilt and verified"), not something pending
   approval.

If you show the developer a rendered preview of the artwork at all (e.g. to
narrate what changed), it must be the *same* image already baked into the
rebuilt app from steps 2-5 — never a separate scratch-only render that steps
2-5 haven't been run against yet. Never show a preview and wait; act first,
then report what you did.

## Why this isn't "wasted work" if the developer wants another revision

Rebuilding is cheap (a few seconds) and scriptable. The cost of *not*
rebuilding — the developer inspecting a stale app or stale icon file and
concluding nothing happened, or losing track of which round is actually
live — is much higher than the cost of one extra `cargo tauri icon` +
`build.sh` cycle per revision. Iterate by applying and rebuilding every
single time, however small the tweak.

## Cleanup

Scratch scripts/PNGs used to generate the artwork belong in the session
scratchpad directory, not the repo — delete them after the real icon set
(`src-tauri/icons/`) has been regenerated from them successfully.

## Design rules (learned from real mistakes made on this icon)

**1. If the developer supplies a reference image to use as the icon
artwork, composite that exact file byte-for-byte — never redraw, retrace,
or "reinterpret" it.** Load it with `Image.open(...)`, and the only
transform allowed on it is a straightforward uniform resize (same aspect
ratio) to fit the target composition. Do not recolor it, redraw its shapes,
"clean it up," or approximate it with hand-drawn primitives, even if it
would look similar — the developer asked for *that specific image*, not a
lookalike.

**2. Never resize, rescale, or reposition the supplied reference image
without being asked — including "shrinking to make room" for something
else you're adding.** This happened once: adding the scenic background
silently shrank the pagoda from its established scale to make the new
background elements fit better, without that shrink being requested. The
fix was to hold the reference image's scale constant (`target_w = int(S *
0.80)`, its size before backgrounds existed) and require any future change
around it to accommodate that scale, not the other way around. If a new
element genuinely can't fit without resizing the reference art, stop and
ask instead of resizing unilaterally.

**3. Never add unrequested styling — outlines, shadows, glows, flourishes,
gradients, extra decorative flair — even if it would plausibly look better.**
This happened once: gold curl flourishes were added flanking the "SQL Dojo"
text without being asked, and had to be removed. The standing instruction
from that correction: *"for this development please only add what i ask to
the best of your ability. there's no need to embellish or improve."* Treat
every icon request as literal scope, not a springboard for "while I'm in
here" improvements. If something seems like it would clearly help (e.g. a
drop shadow for legibility), name it as a suggestion in your reply — don't
just add it.

**4. When a request changes one visual property (size, color, position),
change only that property, by a moderate/reasonable increment — never
combine it with other unrequested changes, and never jump straight to an
extreme value.** This happened once: asked to make the moon "a bit larger,"
it was scaled from ~0.24x to 0.50x canvas width in a single jump — roughly
double — prompting the developer to call out "why did you make such a
drastic increase in size instead of scaling it gradually?" A single
"increase/decrease the size" request should move the value by something in
the neighborhood of 20-40%, not 2x/0.5x, so the developer can steer with
several small corrections instead of overshooting and correcting back.

**5. Font/style choices must avoid unintended cultural or thematic
associations the developer didn't ask for.** This happened once: an initial
font choice (Herculanum) was rejected because its letterforms "implied some
east-asian reference" that was never requested — the ask was for curvature
matching the illustration's style, not any particular cultural motif.
When picking a typeface or decorative style for this icon, sanity-check
what associations its letterforms carry beyond the literal property
requested (curvy, bold, serif, etc.).

**6. Measure, don't eyeball, when a request asks for precise placement.**
This happened once: text was guessed to sit in the roof-face band at
fractions 0.47-0.60 of the reference image's height, and the developer
reported it was "pushed to the top" — the true band, found by scanning the
source PNG's pixel colors column-by-column for the actual color
transitions, was 0.504-0.688. When a request implies exact alignment
("centered between the ridge and gutter," "across the face of the largest
roof"), derive the target coordinates from the actual source image's pixel
data, not a visual guess.
