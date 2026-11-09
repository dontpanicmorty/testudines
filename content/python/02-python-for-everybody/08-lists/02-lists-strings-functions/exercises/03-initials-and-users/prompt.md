Write `senders(lines)`. `lines` is a list of header lines from a made-up mailbox. Lines that begin with `From: ` look like `From: sam@example.org`. Ignore all other lines.

Return a sorted list of the distinct user names (the part before the `@`) found in those lines. Each name appears once even if it was seen several times.
